from odoo import http
from odoo.http import request
from datetime import datetime, timedelta
from werkzeug.exceptions import Forbidden


class InventoryDashboardController(http.Controller):

    @http.route('/inventory_dashboard/data', type='json', auth='user')
    def get_dashboard_data(self, **kwargs):
        if not request.env.user.has_group(
            'inventory_dashboard.group_inventory_dashboard_user'
        ):
            raise Forbidden("Accès non autorisé au dashboard inventaire")

        Picking = request.env['stock.picking']
        Move = request.env['stock.move']

        # Récupérer les paramètres dynamiques (filtres du frontend)
        filters = kwargs.get('filters', {})
        chart_days = filters.get('chart_days', 7)
        recent_days = filters.get('recent_days', 30)
        active_picking_limit = filters.get('active_picking_limit', 50)
        date_from = filters.get('date_from')
        date_to = filters.get('date_to')
        picking_type_id = filters.get('picking_type_id')
        partner_id = filters.get('partner_id')

        # Construire le domaine de base à partir des filtres
        base_domain = []
        if picking_type_id:
            base_domain.append(('picking_type_id', '=', picking_type_id))
        if partner_id:
            base_domain.append(('partner_id', '=', partner_id))

        # Domaine temporel pour les filtres date
        date_domain = []
        if date_from:
            date_domain.append(('scheduled_date', '>=', date_from))
        if date_to:
            date_domain.append(('scheduled_date', '<=', date_to))

        # --- KPI Cards ---

        # 1. Brouillon
        draft_count = Picking.search_count(
            base_domain + date_domain + [('state', '=', 'draft')]
        )

        # 2. En attente
        waiting_count = Picking.search_count(
            base_domain + date_domain + [('state', '=', 'waiting')]
        )

        # 3. Prêts (assigned)
        assigned_count = Picking.search_count(
            base_domain + date_domain + [('state', '=', 'assigned')]
        )

        # 4. Terminés (done, last N days)
        date_n_ago = datetime.now() - timedelta(days=recent_days)
        done_count = Picking.search_count(
            base_domain + [
                ('state', '=', 'done'),
                ('date_done', '>=', date_n_ago.strftime('%Y-%m-%d')),
            ]
        )

        # 5. Annulés
        cancel_count = Picking.search_count(
            base_domain + date_domain + [('state', '=', 'cancel')]
        )

        # 6. En retard
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        late_count = Picking.search_count(
            base_domain + [
                ('state', 'in', ['assigned', 'waiting', 'confirmed']),
                ('scheduled_date', '<', now_str),
            ]
        )

        # 7. Alertes stock min (produits sous le seuil de réapprovisionnement)
        orderpoints = request.env['stock.warehouse.orderpoint'].search_read(
            [], fields=['product_id', 'product_min_qty'],
        )
        low_stock_count = 0
        seen_products = set()
        for op in orderpoints:
            pid = op['product_id'][0]
            if pid in seen_products:
                continue
            seen_products.add(pid)
            quants = request.env['stock.quant'].search([
                ('product_id', '=', pid),
                ('location_id.usage', '=', 'internal'),
            ])
            qty_on_hand = sum(q.quantity for q in quants)
            if qty_on_hand < op['product_min_qty']:
                low_stock_count += 1

        # 8. Mouvements aujourd'hui
        today_start = datetime.now().replace(
            hour=0, minute=0, second=0
        ).strftime('%Y-%m-%d %H:%M:%S')
        today_end = datetime.now().replace(
            hour=23, minute=59, second=59
        ).strftime('%Y-%m-%d %H:%M:%S')
        moves_today_count = Move.search_count([
            ('state', '=', 'done'),
            ('date', '>=', today_start),
            ('date', '<=', today_end),
        ])

        state_counts = {
            'draft': draft_count,
            'waiting': waiting_count,
            'assigned': assigned_count,
            'done': done_count,
            'cancel': cancel_count,
        }

        # --- Types d'opérations ---
        picking_types = request.env['stock.picking.type'].search_read(
            [], fields=['name', 'code', 'color'],
        )
        operation_type_stats = []
        for pt in picking_types:
            pt_domain = [('picking_type_id', '=', pt['id'])]
            pt_draft = Picking.search_count(pt_domain + [('state', '=', 'draft')])
            pt_waiting = Picking.search_count(pt_domain + [('state', '=', 'waiting')])
            pt_assigned = Picking.search_count(pt_domain + [('state', '=', 'assigned')])
            date_7_ago = datetime.now() - timedelta(days=7)
            pt_done = Picking.search_count(pt_domain + [
                ('state', '=', 'done'),
                ('date_done', '>=', date_7_ago.strftime('%Y-%m-%d')),
            ])
            pt_late = Picking.search_count(pt_domain + [
                ('state', 'in', ['assigned', 'waiting', 'confirmed']),
                ('scheduled_date', '<', now_str),
            ])
            operation_type_stats.append({
                'id': pt['id'],
                'name': pt['name'],
                'code': pt['code'],
                'draft': pt_draft,
                'waiting': pt_waiting,
                'assigned': pt_assigned,
                'done': pt_done,
                'late': pt_late,
            })

        # --- Graphique: mouvements de stock par jour ---
        daily_moves = []
        for i in range(chart_days - 1, -1, -1):
            day = datetime.now() - timedelta(days=i)
            day_start = day.replace(
                hour=0, minute=0, second=0
            ).strftime('%Y-%m-%d %H:%M:%S')
            day_end = day.replace(
                hour=23, minute=59, second=59
            ).strftime('%Y-%m-%d %H:%M:%S')
            count = Move.search_count([
                ('state', '=', 'done'),
                ('date', '>=', day_start),
                ('date', '<=', day_end),
            ])
            daily_moves.append({
                'date': day.strftime('%d/%m'),
                'count': count,
            })

        # --- Statistiques résumées ---
        done_pickings_total = Picking.search_count([
            ('state', '=', 'done'),
            ('date_done', '>=', date_n_ago.strftime('%Y-%m-%d')),
        ])
        done_moves_total = Move.search_count([
            ('state', '=', 'done'),
            ('date', '>=', date_n_ago.strftime('%Y-%m-%d')),
        ])

        # --- Table: transferts actifs ---
        active_domain = base_domain + [
            ('state', 'in', ['draft', 'waiting', 'confirmed', 'assigned']),
        ]
        if date_from:
            active_domain.append(('scheduled_date', '>=', date_from))
        if date_to:
            active_domain.append(('scheduled_date', '<=', date_to))

        active_pickings = Picking.search_read(
            active_domain,
            fields=[
                'name', 'picking_type_id', 'partner_id',
                'scheduled_date', 'state',
                'move_type',
            ],
            order='scheduled_date asc',
            limit=active_picking_limit,
        )

        # --- Table: top mouvements par produit ---
        move_domain = [
            ('state', '=', 'done'),
            ('date', '>=', date_n_ago.strftime('%Y-%m-%d')),
        ]
        top_products_data = Move.read_group(
            move_domain,
            fields=['product_id', 'product_uom_qty:sum'],
            groupby=['product_id'],
            orderby='product_uom_qty desc',
            limit=20,
        )
        top_products = []
        for item in top_products_data:
            if item['product_id']:
                top_products.append({
                    'product_id': item['product_id'][0],
                    'product_name': item['product_id'][1],
                    'total_qty': item['product_uom_qty'],
                    'move_count': item['product_id_count'],
                })

        # Config pour le frontend
        config = request.env['inventory.dashboard.config'].get_config()

        return {
            'state_counts': state_counts,
            'late_count': late_count,
            'low_stock_count': low_stock_count,
            'moves_today_count': moves_today_count,
            'operation_type_stats': operation_type_stats,
            'daily_moves': daily_moves,
            'done_pickings_total': done_pickings_total,
            'done_moves_total': done_moves_total,
            'active_pickings': active_pickings,
            'top_products': top_products,
            'config': config,
        }

    @http.route('/inventory_dashboard/filters_data', type='json', auth='user')
    def get_filters_data(self):
        """Retourne les données pour les listes déroulantes des filtres."""
        if not request.env.user.has_group(
            'inventory_dashboard.group_inventory_dashboard_user'
        ):
            raise Forbidden("Accès non autorisé au dashboard inventaire")

        # Types d'opérations
        picking_types = request.env['stock.picking.type'].search_read(
            [], fields=['name'],
        )
        picking_type_list = [
            {'id': pt['id'], 'name': pt['name']}
            for pt in picking_types
        ]

        # Partenaires ayant des transferts
        partners = request.env['stock.picking'].read_group(
            [('partner_id', '!=', False)],
            fields=['partner_id'],
            groupby=['partner_id'],
            limit=200,
        )
        partner_list = [
            {'id': p['partner_id'][0], 'name': p['partner_id'][1]}
            for p in partners if p['partner_id']
        ]

        return {
            'picking_types': picking_type_list,
            'partners': partner_list,
        }
