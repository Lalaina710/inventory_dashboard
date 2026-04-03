{
    'name': 'Tableau de bord Inventaire',
    'version': '18.0.2.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Dashboard Inventaire dynamique avec KPI, filtres et configuration',
    'description': 'Tableau de bord interactif pour le suivi des opérations de stock avec filtres dynamiques, rafraîchissement auto et configuration.',
    'author': 'SOPROMER',
    'depends': ['stock'],
    'data': [
        'security/inventory_dashboard_groups.xml',
        'security/ir.model.access.csv',
        'views/inventory_dashboard_config_views.xml',
        'views/inventory_dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'inventory_dashboard/static/src/css/inventory_dashboard.css',
            'inventory_dashboard/static/src/xml/inventory_dashboard.xml',
            'inventory_dashboard/static/src/js/inventory_dashboard.js',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
