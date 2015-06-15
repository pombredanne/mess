'''
ILFDataLoader.py

Created on Jul 9, 2012

@author: f2916479

$Id:$
'''

from FcnLogger import FcnLogger
#from ILFConfig import ILFConfig
import MySQLdb
import shutil
import datetime
import os
import fnmatch

class ILFDataLoader(object):
    '''
    Loads data from file into the database by invoking the mysqlimport utility.
    
    STEPS:
    1:    Rename the file to be processed to <filename>.processing
    2:    Import the file.
    3:    Rename the file to the current day <filename>_YYYY_MM_DD
    4:    Runs SQL statements to update fields
    
    It will not remove the <filename>_processing file should there be an error.
    '''

    _LOAD_STMT = 'LOAD DATA INFILE \'%s.processing\' '+ \
                 'IGNORE INTO TABLE admin.ilf_eod_summary '+ \
                 '(@line) '+ \
                 'SET '+ \
                 'fin_ind = SUBSTR(@line,201,1),'+ \
                 'record_type = SUBSTR(@line,202,5),'+ \
                 'from_company_id = SUBSTR(@line,207,5),'+ \
                 'from_product = SUBSTR(@line, 212, 3),'+ \
                 'from_account = SUBSTR(@line, 215, 23),'+ \
                 'fnb_company_Id = SUBSTR(@line, 238, 5),'+ \
                 'fnb_product = SUBSTR(@line, 243, 3),'+ \
                 'fnb_account = SUBSTR(@line, 246, 23),'+ \
                 'fin_amount = SUBSTR(@line, 269, 15),'+ \
                 'topup_amount = SUBSTR(@line, 284, 15),'+ \
                 'vat_amount = SUBSTR(@line, 299, 15),'+ \
                 'discount_amount = SUBSTR(@line, 314, 15),'+ \
                 'discount_percentage = SUBSTR(@line, 329, 5),'+ \
                 'vods_trace_id = SUBSTR(@line, 334, 12),'+ \
                 'business_date = SUBSTR(@line, 346, 8),'+ \
                 'creditcard_sequence_no = SUBSTR(@line, 354, 12);'

    _SQL_UPDATE_1 = 'update admin.fin_log_eod fle, admin.ilf_eod_summary ies '+ \
                    ' set fle.match_count = 1 '+ \
                    ' where fle.match_count = 0 '+ \
                    ' and (fle.vods_trace_id = ies.vods_trace_id or fle.fin_value = 0);'

    _SQL_UPDATE_2 = 'update admin.fin_log_eod fle, admin.ilf_eod_summary ies '+ \
                    ' set ies.run_id = 1, ies.match_result = \'matched\''+ \
                    ' where ies.run_id = 0 and fle.vods_trace_id = ies.vods_trace_id;'

    def __init__(self):
        '''
        Constructor
        '''
        self.logger = FcnLogger.getInstance()
        self.config = ILFConfig.getInstance()

    def loadData(self, filename):
        '''
        Reads the file in and writes each record into the table
        '''
        connection = None
        cursor = None
        # filename = "%s/%s" % (self.config.getDirectory(), self.config.getFilename())

        try:
            self.logger.info("ILFDataLoader: processing file: %s" % filename)
            shutil.move(filename,
                        filename + ".processing")

            self.logger.info("Creating DB Connection to: %s:%s" % (self.config.getDbHost(), self.config.getDbPort()))

            connection = MySQLdb.Connection(self.config.getDbHost(),
                                            user=self.config.getDbUser(),
                                            port=self.config.getDbPort(),
                                            passwd=self.config.getDbPass(),
                                            db=self.config.getDbSchema())

            cursor = connection.cursor()
            self.logger.debug(self._LOAD_STMT % filename)
            cursor.execute(self._LOAD_STMT % filename)
            self.logger.info("ILFDataLoader: file loaded: %s.processing" % (filename))

            # Run updates
            self.logger.info("ILFDataLoader: running update 1: %s.processing" % (filename))
            cursor.execute(self._SQL_UPDATE_1)
            self.logger.info("ILFDataLoader running update 2: %s.processing" % (filename))
            cursor.execute(self._SQL_UPDATE_2)

            self.logger.info("ILFDataLoader: Moving file: %s.%s" % (filename + ".processing",
                        filename + "_" + datetime.datetime.today().strftime('%y%m%d%H%M')))
            shutil.move(filename + ".processing",
                        filename + "_" + datetime.datetime.today().strftime('%y%m%d%H%M'))

            self.logger.info("ILFDataLoader: complete: %s" % filename)

            # Close connections
            cursor.close()
            connection.close()
        except MySQLdb.Error, e:
            if( e.args[0] == 1062):
                # Ignore this error as the file was previously imported. Ignore the file.
                self.logger.warn("ILFDataLoader: ignoring previously imported file: %s" % filename)
            else:
                self.logger.error("MySQLdb.Error: %s : %s" % (args[0], args[1]))
                raise e

        except IOError, e:
            self.logger.error("ILFDataLoader: IO Exception processing file: %s" % e.args[0])
            raise e

        except Exception, e:
            self.logger.error("ILFDataLoader: Exception processing file: %s" % e.args[0])
            raise e


            #       finally:
            #           if(cursor != None):
            #               cursor.close()
            #
            #           if(connection != None):
            #               connection.close()

    def processFile(self):
        try:
            self.logger.info("ILFDataLoader: Scanning for files to process in : %s" % self.config.getDirectory())
            for filename in os.listdir(self.config.getDirectory()):
                self.logger.info("Checking file: %s" % filename)
                if(fnmatch.fnmatch(filename, self.config.getFilename())):
                    try:
                        self.logger.info("ILFDataLoader: Found file to process [%s]" % filename)
                        self.loadData("%s/%s" % (self.config.getDirectory(), filename))

                    except Exception, e:
                        self.logger.error("ILFDataLoader: IO Exception processing file: %s" % e.args[0])
                        shutil.move(filename + ".processing",
                                    filename)
                        raise e
            self.logger.info("ILFDataLoader: Finished processing scanned files...")
        except Exception, e:
            self.logger.error("Aborting load: %s" % e.args[0])
            raise e


if __name__ == '__main__':
    load = ILFDataLoader()
    load.processFile()


