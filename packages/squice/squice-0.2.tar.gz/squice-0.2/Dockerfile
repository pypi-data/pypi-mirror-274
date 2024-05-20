######################################################################################################
### Correctly set up the .github/workflows/docker.yml will update this to docker automatically. ###
#######################################################################################################
### To build this manually ###
# docker build -f Dockerfile -t raea/squice .
# 
### To run it manually ###
# docker run --rm --name squice -p 8001:8501 raea/squice
#
# I can then be found at http://localhost:8201/
# 
### To push it manually ###
# docker push raea/squice
######################################################################################################

FROM python:3.10
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["app/home.py"]
