import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
cur = conn.cursor()

def create_table():
	cur.execute('CREATE TABLE IF NOT EXISTS blogtable(author TEXT,title TEXT,article TEXT,postdate,DATE)')


def add_data(author,title,article,postdate):
	cur.execute('INSERT INTO blogtable(author,title,article,postdate) VALUES (?,?,?,?)',(author,title,article,postdate))
	conn.commit()


def view_all_notes():
	cur.execute('SELECT * FROM blogtable')
	data = cur.fetchall()
	# for row in data:
	# 	print(row)
	return data


def view_all_titles():
	cur.execute('SELECT DISTINCT title FROM blogtable')
	data = cur.fetchall()
	# for row in data:
	# 	print(row)
	return data


def get_single_blog(title):
	cur.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = cur.fetchall()
	return data


def get_blog_by_title(title):
	cur.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
	data = cur.fetchall()
	return data


def get_blog_by_author(author):
	cur.execute('SELECT * FROM blogtable WHERE author="{}"'.format(author))
	data = cur.fetchall()
	return data


def get_blog_by_msg(article):
	cur.execute("SELECT * FROM blogtable WHERE article like '%{}%'".format(article))
	data = cur.fetchall()
	return data


def edit_blog_author(author,new_author):
	cur.execute('UPDATE blogtable SET author ="{}" WHERE author="{}"'.format(new_author,author))
	conn.commit()
	data = cur.fetchall()
	return data


def edit_blog_title(title,new_title):
	cur.execute('UPDATE blogtable SET title ="{}" WHERE title="{}"'.format(new_title,title))
	conn.commit()
	data = cur.fetchall()
	return data


def edit_blog_article(article,new_article):
	cur.execute('UPDATE blogtable SET title ="{}" WHERE title="{}"'.format(new_article,article))
	conn.commit()
	data = cur.fetchall()
	return data

def delete_data(title):
	cur.execute('DELETE FROM blogtable WHERE title="{}"'.format(title))
	conn.commit()
