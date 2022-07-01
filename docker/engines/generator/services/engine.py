import os
from dags import generator_dag
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description="Invoice Generator"
    )

    parser.add_argument("--max-invoices", required=True)
    parser.add_argument("--max-items", required=True)
    parser.add_argument("--quantity", required=True)
    args = parser.parse_args()
    
    generator_dag\
        .execute_dag(
            max_invoices=int(args.max_invoices),
            max_items=int(args.max_items),
            quantity=int(args.quantity)
    )