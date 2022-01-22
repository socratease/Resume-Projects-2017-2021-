########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = True

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "cgraves36"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = """
        CREATE TABLE movies (
        	id INTEGER,
        	title TEXT,
        	score REAL
        	);"""
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = """
        CREATE TABLE movie_cast (
        	movie_id INTEGER,
        	cast_id INTEGER,
            cast_name TEXT,
            birthday TEXT,
        	popularity REAL
        	);"""
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    def execute_manyquery(self, connection, query, dat):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.executemany(query, dat)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
    
        with open(path) as csv_file:
            reader = csv.reader(csv_file)
    
            moviedata = list()
            for row in reader:
                moviedata.append(row)
                
            q = 'INSERT INTO movies (id, title, score) VALUES (?,?,?)'
            self.execute_manyquery(connection, q, moviedata)
       ######################################################################
        
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open(path) as csv_file:
            reader = csv.reader(csv_file)
    
            moviecastdata = list()
            for row in reader:
                moviecastdata.append(row)
                
            q = '''INSERT INTO movie_cast (movie_id, cast_id, cast_name, birthday, popularity)
                        VALUES (?,?,?,?,?)'''
            self.execute_manyquery(connection, q, moviecastdata)
        ######################################################################
        
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = """
        CREATE TABLE cast_bio (
        	cast_id INTEGER,
            cast_name TEXT,
            birthday DATE,
        	popularity REAL
        	);"""
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW #############################
        
        part_aiii_insert_sql = """
        INSERT INTO cast_bio (cast_id, cast_name, birthday, popularity)
        SELECT DISTINCT cast_id, cast_name, birthday, popularity FROM movie_cast
        ;"""
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = "CREATE INDEX movie_index ON movies(id)"
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql = "CREATE INDEX cast_index ON movie_cast(cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = "CREATE INDEX cast_bio_index ON cast_bio(cast_id)"
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = """
        SELECT printf('%.2f', 100 * SUM(CASE WHEN (score > 50 AND upper(TITLE) LIKE '%WAR%') THEN 1.0 ELSE 0.0 END) / COUNT(id))
        FROM movies"""
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = """
        SELECT cast_name, count(*) as appearance_count
        from movie_cast
        WHERE popularity > 10
        GROUP BY cast_name
        ORDER BY appearance_count DESC, cast_name
        LIMIT 5
        """
#        """
#        WITH goodmovies (cast_name, movie_id) as (SELECT cast_name, movie_id FROM movie_cast WHERE popularity > 10)
#        SELECT cast_name, count (movie_id) as appearance_count
#        from goodmovies
#        GROUP BY cast_name
#        ORDER BY appearance_count DESC, cast_name
#        LIMIT 5
#        """
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_e_sql = """
        WITH castsize(movie_id, cast_count) AS (SELECT movie_id, count(cast_id) FROM movie_cast GROUP BY movie_id)
        SELECT movie_title, printf('%.2f', score) as movie_score, cast_count FROM (
        SELECT m.title as movie_title, m.score, c.cast_count as cast_count
        FROM movies m INNER JOIN castsize c on m.id = c.movie_id
        ORDER BY score DESC, cast_count ASC, movie_title ASC
        )
        LIMIT 5
        """
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_f_sql = """
        WITH moviescores(id, score) as (SELECT id, score FROM movies WHERE score >= 25)
        SELECT cast_id, cast_name, printf('%.2f', average_score) as average_score from (
        SELECT c.cast_id, c.cast_name, avg(m.score) as average_score
        from movie_cast c INNER JOIN moviescores m on c.movie_id = m.id
        GROUP BY c.cast_id, c.cast_name
        HAVING COUNT(c.cast_id) > 2
        ORDER BY average_score DESC, cast_name)
        LIMIT 10
        """
        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = """
        CREATE VIEW good_collaboration (
            cast_member_id1,
            cast_member_id2,
            movie_count,
            average_movie_score)
        AS
            SELECT actor1 as cast_member_id1, actor2 as cast_member_id2, ct as movie_count, score as average_movie_score
            FROM
            	(
            	SELECT actor1, actor2, count(*) as ct, avg(score) as score from 
            		(
            		Select c1.movie_id, c1.cast_id as actor1, c2.cast_id as actor2, m.score
            		from movie_cast c1
            		INNER JOIN movie_cast c2 ON c1.movie_id = c2.movie_id
            		INNER JOIN movies m on c1.movie_id = m.id
            		WHERE c1.cast_id < c2.cast_id
            		)
            	GROUP BY actor1, actor2
            	)
            WHERE movie_count >= 3
			AND score >= 40
        """
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql = """
        with c1 as (
        	select cast_member_id1 as id,
        	count(*) as movs,
        	sum(average_movie_score) as pts
        	from good_collaboration
        	group by cast_member_id1),
        	
        c2 as (
        	select cast_member_id2 as id,
        	count(*) as movs,
        	sum(average_movie_score) as pts
        	from good_collaboration
        	group by cast_member_id2),
        	
        joined as (
        	select * from c1
        	UNION ALL
        	select * from c2),
        
        joinsum as (
        	select id as cast_id,
        	sum(movs) as movs,
        	sum(pts) as pts
        	from joined
        	group by id)
        	
        select j.cast_id,
        	c.cast_name,
        	printf( '%.2f', j.pts / j.movs) as collaboration_score
        from joinsum j
        left join (select distinct cast_id, cast_name from movie_cast) c on j.cast_id = c.cast_id
        order by collaboration_score desc, cast_name
        limit 5
        """
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = """
        
        CREATE VIRTUAL TABLE movie_overview USING fts3(
                id INTEGER,
                overview TEXT)
       
        

        """
        ######################################################################
        connection.execute(part_h_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        
        with open(path) as csv_file:
            reader = csv.reader(csv_file)
    
            moviedata = list()
            for row in reader:
                moviedata.append(row)
                
            q = 'INSERT INTO movie_overview (id, overview) VALUES (?,?)'
            self.execute_manyquery(connection, q, moviedata)
            
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = "SELECT count(*) FROM movie_overview WHERE overview MATCH 'fight'"
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = "SELECT count(*) FROM movie_overview WHERE overview MATCH 'space NEAR/5 program'"
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    try:
        print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
        print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    except:
         print("Error in Part a.i")

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    except:
        print("Error in part a.ii")

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    except:
        print("Error in part a.iii")

    try:
        print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
        print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
        print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    except:
        print("Error in part b")

    try:
        print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    except:
        print("Error in part c")

    try:
        print('\033[32m' + "part d: " + '\033[m')
        for line in db.part_d(conn):
            print(line[0],line[1])
    except:
        print("Error in part d")

    try:
        print('\033[32m' + "part e: " + '\033[m')
        for line in db.part_e(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part e")

    try:
        print('\033[32m' + "part f: " + '\033[m')
        for line in db.part_f(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part f")
    
    try:
        print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
        print('\033[32m' + "part g.i: " + '\033[m')
        for line in db.part_gi(conn):
            print(line[0],line[1],line[2])
    except:
        print("Error in part g")

    try:   
        print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    except:
        print("Error in part h")

    conn.close()
    #################################################################################
    #################################################################################
  
