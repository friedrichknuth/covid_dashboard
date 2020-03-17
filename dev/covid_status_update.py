import smtplib
from email.message import EmailMessage
import imghdr
import pandas as pd
import matplotlib.pyplot as plt
import datetime

recipients = ['']
email = ''
auth = ''

src = 'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'

df = pd.read_csv(src)
df = df[df['Country/Region'] == 'US']
df_counties = df[df['Province/State'].str.contains(',')]
df_counties = df_counties.groupby(['Country/Region'], as_index=False).sum()
df_counties = df_counties.drop(['Lat', 'Long'], axis=1)
df_counties = df_counties.T
df_counties = df_counties.drop(['Country/Region'])
df_counties = df_counties.reset_index()
df_counties = df_counties.truncate(after=47)
df = df[~df['Province/State'].str.contains(',')]
df = df[~df['Province/State'].str.contains('Princess')]
df = df.groupby(['Country/Region'], as_index=False).sum()
df = df.drop(['Lat', 'Long'], axis=1)
df = df.T
df = df.drop(['Country/Region'])
df = df.reset_index()
df = df.truncate(before=48)
df = df_counties.append(df)
count = df[0].values[-1]
df = df.set_index(['index'])
df.columns = ['US']
df.index.name = 'Date'

fig,ax = plt.subplots(figsize=(10,10))
df.plot(ax = ax)
patches, labels = ax.get_legend_handles_labels()
ax.legend(patches, labels, loc='upper left')
ax.set_title('Confirmed cases as of ' + datetime.datetime.today().strftime("%Y-%m-%d"))
fig.savefig("plot.png")

img_data = open('plot.png', 'rb').read()
msg = EmailMessage()

image_cid = 'https://img.shields.io/static/v1.svg?logo=Jupyter&label=Launch+App&message=AWS+us-west-2&color=green'

msg.add_alternative("""\
<html>
    <body>
    <a href="https://aws-uswest2-binder.pangeo.io/v2/gh/friedrichknuth/covid_dashboard/binder-app?urlpath=/proxy/5006/dashboard-panel"><img src="{image_cid}"></a>
    </body>
</html>
""".format(image_cid=image_cid), subtype='html')

msg.add_attachment(img_data, maintype='image',
                                 subtype=imghdr.what(None, img_data))

msg['Subject'] = 'Confirmed cases: ' + str(count)

recipients = recipients
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(email, auth)
server.sendmail(email,recipients,msg.as_string())
server.quit()
