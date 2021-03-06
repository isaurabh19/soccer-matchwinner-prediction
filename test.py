import sys
import xlrd
import xlwt
from featureComp import *
from createmat import *



def findRank(path2):
	for i in range(1,39):
		path3=path2+"/Match"+str(i)+'.xlsx'
		matchday= xlrd.open_workbook(path3)
		sheet1=matchday.sheet_by_index(0)
		#print path3,'\n'
		for j in range(1,21):
			team_rank[sheet1.cell(j,2).value.strip()].append(sheet1.cell(j,0).value)


def resetMatches(matches_played):
    for k in matches_played.keys():
        matches_played[k]=0
teams={}
matches_played={}
team_rank={}
teamprofile={}
train_book= xlwt.Workbook()
sheet1=train_book.add_sheet("sheet 1")
book =xlrd.open_workbook("/home/saurabh/projects/football/Season_table.xlsx")
first_sheet = book.sheet_by_index(0)
form_table=([0.75,0.15,20],[0.6,0.25,16],[0.4,0.4,12],[0.15,0.6,10])
for i in range(1,37):
	teams[first_sheet.cell(i,0).value.strip()]=[]
	matches_played[first_sheet.cell(i, 0).value.strip()]=0
	teamprofile[first_sheet.cell(i,0).value.strip()]=[]
	team_rank[first_sheet.cell(i,0).value.strip()]=[]
num=2005
match=1
featureobj=Feature()
fbook= xlrd.open_workbook(sys.argv[1])
first_sheet = fbook.sheet_by_index(0)
findRank(sys.argv[2])
AQDQmat(first_sheet,teams)
FORMmat(first_sheet, team_rank, teams, matches_played, form_table)
resetMatches(matches_played)
featureobj.featureCompute(first_sheet,sheet1,teams,matches_played,teamprofile)
num+=1
train_book.save("/home/saurabh/projects/football/testset.xls")
rtrain_book=xlrd.open_workbook('/home/saurabh/projects/football/testset.xls')
svmdatasheet=rtrain_book.sheet_by_index(0)
with open('/home/saurabh/projects/football/wekarealtest.arff', 'w') as f:
    featureobj.WEKAformat(svmdatasheet,f)
f.closed