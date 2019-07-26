# create a data frame of games before a certain date
def create_dataframe (team,date,file):
    rows=file.loc[file['Team'] == team]
    dates=[]
    for value in rows['Game Date'].values:
        if datecomp(value,date)==value:
            dates.append(rows.loc[rows['Game Date']==value])
    if dates == []:
        return 0
    else:
        data=dates[0]
        data=data.append(dates[0:len(dates)]) #REPEATING A ROW/ RUN TO RESOLVE
        return data.drop(data.index[0])

# get averages for each team        
def get_avgs(dataframe,columns):
  dataframe=dataframe.iloc[list(range(47))]
  avgs=[]
  for column in columns:
    divider=0
    count=0
    for x in dataframe[column]:
      count=count + int(x)
      divider=divider+1
    avg=float(count/divider)
    avgs.append(avg)
  return avgs

def create_winrate(team,date,file):
    rows=file.loc[file['Team'] == team]
    dates=[]
    for value in rows['Game Date'].values:
        if datecomp(value,date)==value:
            dates.append(rows.loc[rows['Game Date']==value])
    if dates == []:
        return 0
    else:
        data=dates[0]
        data=data.append(dates[0:len(dates)])#REPEATING A ROW/ RUN TO RESOLVE
        data =data.drop(data.index[0])
        try:
            data=data.iloc[list(range(47))]
            b=0
            for x in data['W/L'].values:
                if x == 'W':
                    b=b+1
            return float(b/len(data))*100
        except:
            return 12345 #bandage to fix last 69 games of file

#create a function to determine if a date is sooner than another date
def datecomp(date1,date2):
    if date1[6:len(date1)]>date2[6:len(date2)]:
        #print("date1's year is greater than date2's year")
        return date2
    if date1[6:len(date1)]<date2[6:len(date2)]:
        #print("date2's year is greater than date1's year")
        return date1
    
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]>date2[3:5]:
            #print("date1's month is greater than date2's month")
            return date2
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]<date2[3:5]:
            #print("date2's month is greater than date1's month")
            return date1
        
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]==date2[3:5]:
            if date1[0:2]>date2[0:2]:
                #print("date1's day is greater than date2's day")
                return date2
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]==date2[3:5]:
            if date1[0:2]<date2[0:2]:
                #print("date2's day is greater than date1's day")
                return date1
            
    if date1[6:len(date1)]==date2[6:len(date2)]:
        if date1[3:5]==date2[3:5]:
            if date1[0:2]==date2[0:2]:
                return 0

