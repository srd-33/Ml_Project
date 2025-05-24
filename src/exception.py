import sys
from src.logger import logging

def err_msg_detail(err,err_details:sys):

   _,_,err_tb= err_details.exc_info()

   file_name = err_tb.tb_frame.f_code.co_filename
   err_msg = "Error occured in filename [{0}], in line no [{1},error mesage[{2}]]".format(
       file_name,err_tb.tb_lineno,str(err)
   )

   return err_msg

class CustonException(Exception):
    def __init__(self, err_msg, err_details:sys):
        super().__init__(err_msg)
        self.err_msg = err_msg_detail(err_msg,err_details=err_details)

    def __str__(self):
        return self.err_msg
    
if __name__ =="__main__":

    try:
        a=1/0
    except Exception as e:
        logging.info("Division by zero")
        raise CustonException(e,sys)
