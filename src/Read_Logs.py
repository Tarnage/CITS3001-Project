import os



class Read_Logs:
    def __init__(self) -> None:
        self.results =  {
                            "red": {
                                "turn": {}
                            },
                            "blue": {
                                "turn": {}
                            },
                            "green": {
                                "turn": {}
                            },
                            "grey": {
                                "team":{
                                    "blue": {},
                                    "red": {}
                                }
                            }
                        }


    def read_logs(self, log: str):

        with open(log, 'r') as input:
            pass

    
    def read_all_logs(self, path: str):
        
        # Change the directory
        os.chdir(path)

        # iterate through all file
        for file in os.listdir():
            # Check whether file is in text format or not
            if file.endswith(".log"):
                file_path = f"{path}\{file}"
        
                # call read text file function
                self.read_logs(file_path)
        