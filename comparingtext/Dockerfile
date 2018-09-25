# Using lightweight alpine image
FROM python:3.6-alpine

# Installing packages



RUN apk update
RUN apk upgrade

RUN echo "http://nl.alpinelinux.org/alpine/v3.6/main" >> /etc/apk/repositories

#RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
####RUN pip install --no-cache-dir numpy scipy pandas matplotlib



RUN pip install --no-cache-dir pipenv

RUN pip install --no-cache-dir numpy

RUN pip install --no-cache-dir stop-words

#RUN pip install --no-cache-dir scipy

RUN pip install scipy==0.13.3

#RUN apk del scipy-build
#RUN apk add --virtual scipy-runtime 

RUN pip install --no-cache-dir -U scikit-learn

RUN pip install -U nltk

RUN pip install Flask

RUN pip install -U flask-cors

#RUN export PATH=/usr/lib/postgresql/X.Y/bin/:$PATH

#RUN apk add postgresql-dev

#RUN pip install psycopg2



# Defining working directory and adding source code
WORKDIR /usr/src/app
#COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY Pipfile Pipfile.lock bootstrap.sh ./

RUN chmod +x bootstrap.sh
COPY comparingtext ./comparingtext


# Install API dependencies
#RUN pipenv install

# Start app
EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]




