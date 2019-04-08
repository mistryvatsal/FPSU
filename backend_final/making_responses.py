import json
import re

from sentiment_analysis.sentiment import sentiment_return
def function(arg):
    print()
try:
    arg='default_students_responses'
    f=open('responses/'+arg+'.json')
    data=json.load(f)
    f.close()
    #print(len(data))
except:
    print('error fetching file details')
#  [u'41', u'51', u'61', u'71', u'81', u'101', u'111', u'141']
#print(data)
main_list=[]
main_list_reasons=[]
for i in data:
    list_in=[]
    list_reasons=[]
    list_temp=[]
    for j in data[i]:
        #print(j)
        list_temp.append((j[1:]))

    list_temp=sorted(list_temp,key=int)
    #print(list_temp)
    for k in list_temp:
        try:
            #print()
            list_reasons.append(data[i]['q'+k]['negate']['data'])
        except: pass
        list_in.append(data[i]['q'+k]['data'])
    #print(list_in)
    main_list_reasons.append(list_reasons)
    main_list.append(list_in)
    #print()
    #for j in data[i]:


print(main_list)
print('reasons',main_list_reasons)

final_sent_values=sentiment_return(main_list)
print(final_sent_values)

