# Run docker build from the project root, outside the /src folder
# Use: docker build -t datalyzer-datacollection -f src/datacollection/Dockerfile .

FROM python:3.11.9
COPY src/datacollection/DCrequirements.txt .
RUN pip install -r DCrequirements.txt
COPY src/DCMain.py .
COPY src/datacollection ./datacollection/
ENTRYPOINT ["python", "DCMain.py"]
EXPOSE 443/tcp