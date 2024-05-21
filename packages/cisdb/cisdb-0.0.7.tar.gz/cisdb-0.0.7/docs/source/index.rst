.. cisdb documentation master file, created by
   sphinx-quickstart on Wed Jul  1 10:45:10 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CISdb Channel Information System database support
=================================================

CISdb is a package of database support libraries and programs.
The libraries contain classes representing tables in the
database.  The programs build tables from frame files, NDS2,
and hopefully DAQ config files.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Database schema
***************

The tables and colums are shown at
https://ldas-jobs.ligo.caltech.edu/~joseph.areeda/cis/cis-tables.html

The design is different from the previous vrevious implementation:

* All manually entered descriptions are kept in a separate
  table. This allows us to delete and recreate the automatically
  generate tables.
* We use lista to store various attributes.  These are serialized
  as JSON arrays and stored as a text column.
* The channel table contains entries from frames and NDS2.
* The fragment table contains the entris from the fragment
  column to allow easy searching.
* The ifo tble contains information from frames.

Examples
--------

Channel table entry::

   mysql> select * from Channels where name = 'IMC-MC2_TRANS_YAW_OUT_DQ'\G
   *************************** 1. row ***************************
             id: 78386
           name: IMC-MC2_TRANS_YAW_OUT_DQ
     chan_types: ["ONLINE", "RAW"]
     data_types: ["REAL_4"]
            ifo: ["L1", "H1"]
      subsystem: IMC
      fragments: ["MC2", "TRANS", "YAW", "OUT", "DQ"]
        cluster: ["LLO", "CIT"]
   sample_rates: [2048.0]
          unitX: ["time"]
          unitY: ["undef"]
         frames: ["H-H1_R", "L-L1_R"]
           gain: NULL
          slope: [1.0]
         offset: [0.0]
     is_current: NULL
   1 row in set (0.00 sec)

Get any applicable descriptions::

   mysql> select * from Descriptions where name regexp '^(IMC-MC2_TRANS_YAW_OUT_DQ|MC2|TRANS|YAW|OUT|DQ)$'\G
   *************************** 1. row ***************************
             id: 2
           name: IMC-MC2_TRANS_YAW_OUT_DQ
   descriptions: ["MC2 transmitting port QPD yaw error signal", "<img src=\"https://ldas-jobs.ligo.caltech.edu/~laura.nuttall/cis/IMC_layout.png\">"]
   *************************** 2. row ***************************
             id: 551
           name: OUT
   descriptions: ["Output Filter Bank"]
   *************************** 3. row ***************************
             id: 552
           name: DQ
   descriptions: ["Raw Channel Recorded by Data Acquisition System"]
   *************************** 4. row ***************************
             id: 577
           name: MC2
   descriptions: ["The second mirror of the input mode cleaner"]
   *************************** 5. row ***************************
             id: 578
           name: TRANS
   descriptions: ["Transmitting port"]
   *************************** 6. row ***************************
             id: 581
           name: YAW
   descriptions: ["yaw"]
   6 rows in set (0.01 sec)

Information on an IFO obtained from frames::

   mysql> select * from IFOs where name='H1'\G
   *************************** 1. row ***************************
            id: 2
          name: H1
      detector: LHO_4k
      latitude: 0.810795247554779
     longitude: -2.0840768814086914
     elevation: 142.5540008544922
      Xazimuth: 5.654877185821533
      Yazimuth: 4.084080696105957
     Xaltitude: -0.0006195000023581088
     Yaltitude: 0.00001249999968422344
     Xmidpoint: 1997.5419921875
     Ymidpoint: 1997.52197265625
   description: NULL
   1 row in set (0.00 sec)



Class libraries
***************

cisdb
------

The **cisdb** library contains subclasses of **Table** and
**Row** classes in the **basedb** library. Most application
level programs will deal with tese classes.

* **CisDB** is a top level class to start accessing the
  database.Once the object is created with login information
  a Database, ChannelTable, IfoTable, FragmentTable, and
  Descriptions instances are available as attributes.





basedb
------
The **basedb** library is independent of any specific
database or tables. It defines the following classes. Only
some methods are highlighted here.

* **Database** represents a MariaDB/MySQL connection.
  Multiple objects
  of this class can be useful. Available methods include:

  * **execute** runs an SQL statement that doesn't return
    a list of results.
  * **execute_query** runs an SQL query and returns an open
    **cursor** object
  * **Database.getlogger** a static method to allow all of
    the cisdb module to use a single logger.
* **Table** is a base class representing a generic table in the
  database.  Subclasses define specific tables. These are
  some of the major methods for Table objects are:

  * **read** rows selecting, ordering, options are available.
  * **insert** a single or list of new rows.
  * **update** a single or list of existing rows.
  * **create** and **drop** tables.

* **Row** is a base class representing a generic row in a table.
  Subclasses define the contents of specific tables. The base
  class encodes and decodes our extensions to database classes
  such as Python lists are transparently stored as JSON arrays
  in catabase text columns.

  * **define_cols** takes a list of Column objects to populate
    internal data structures
  * **set_eq_cols** defines which columns to test for
    equality
  * **set** adds values to a list of columns.
  * **needs_update** uses the "eq colums" to determine if the
    other row has new information
  * **merge** Adds new information from the other row to this
    object. Fills null colummns, appends to lists or raises
    an exception on a conflict.

* **Column** defines a row member representing a value.
  Initialized with a dictionary defining attributes like data
  type, default value, indexing options, whether unique values
  are demanded. This class is rarely needed at higher levels
  since the conversions needed to read/write rows in db are
  done transparently.

  * **get_column_def** returns the SQL to define this column
    when creating the table
  * **get_dbtype** converts Python types to SQL types
  * **get_db_val** converts the Python value to SQL value
  * **get_ret_val** converts the SQL value to Python value

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
