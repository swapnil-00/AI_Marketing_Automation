import os

def run_main_py():
    os.system('python main.py')

def run_app_py():
    os.system('streamlit run app.py')

def main():
    run_main_py() 
    run_app_py()  

if __name__ == "__main__":
    main()
