# Cloudflare Worker URL
WORKER_URL = "https://collection-form.southlinks.workers.dev"

# Form settings
PLUGIN_OPTIONS = [
    "Deposit Plugin",
    "Fix Asset Plugin",
    "Shipment Plugin",
    "Stock Request Plugin",
    "Doc Control Plugin"
]

# Implementation options
IMPLEMENTATION_OPTIONS = [
    "SALES ORDER",
    "DELIVERY ORDER",
    "SALES INVOICE",
    "PICKING LIST",
    "PURCHASE ORDER",
    "CASH SALES",
    "QUOTATION",
    "OFFICIAL RECEIPT",
    "PAYMENT VOUCHER"
]

# Master data options
MASTER_DATA_OPTIONS = [
    "CHART OF ACCOUNT",
    "DEBTOR",
    "CREDITOR",
    "STOCK ITEM"
]

# Migration options
MIGRATION_OPTIONS = [
    "DEBTOR AGING",
    "CREDITOR AGING",
    "TRIAL BALANCE REPORT",
    "BALANCE SHEET REPORT",
    "STOCK BALANCE",
    "SO/PO OUTSTANDING"
]

STATUS_OPTIONS = ["pending", "complete", "AR/Ap, Stock pending"]