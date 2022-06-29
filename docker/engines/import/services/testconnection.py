from hooks.mariadb_hook import MariaDBHook

if __name__=='__main__':
    hook = MariaDBHook(
            database="DB_TEST",
            host="mysql",
            port="3307",
            user="root",
            password="pw_root"
    )
    
    print(hook.get_tables())
    