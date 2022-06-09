from dags.invoices_dag import invoice_dag


if __name__=='__main__':
    for i in range(1, 11):
        invoice_dag(i,
                    100000*i,
                    1,
                    10)
        