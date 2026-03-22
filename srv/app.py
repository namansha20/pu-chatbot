import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class PoornimaUniversityBot:
    def getDataFrame(self, file_path):
        try:
            df = pd.read_excel(file_path)
            df = df.dropna(subset=['Question', 'Answer'])
            df = df.reset_index(drop=True)
            return df
        except Exception as e:
            print(f"Error reading the file: {e}")
            return pd.DataFrame(columns=['Question', 'Answer'])
    
    def process_questions(self, user_input, data_frame):
        #for simplicity, we will just echo back the question
        print(f"YOU ASKED: {user_input}")

        if data_frame.empty:
            return "I don't have training data available right now. Please try again later."

        #get all questions in list
        questions = data_frame['Question'].tolist()
        print(f"ALL QUESTIONS: {questions}")
        ##add users question as first line
        questions.append(user_input)
        ##calculate tf-idf for all data
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(questions)
        #print the matrix
        print(tfidf_matrix.toarray())
        #cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

        if cosine_sim.size == 0:
            return "I could not find a matching answer in the dataset."

        #index of the line no. of record with most similar
        most_similar_index = cosine_sim.argmax()
        print(f"MOST SIMILAR INDEX: {most_similar_index}")

        #remove question from dataset
        questions.pop()

        #return the answers
        answer = data_frame.iloc[most_similar_index]['Answer']
        print(f"ANSWER: {answer}")

        #return the matrix
        return answer

class InputQuestion(BaseModel):
    question: str

class InputBody(BaseModel):
    input: InputQuestion

app = FastAPI()
pu_bot = PoornimaUniversityBot()

@app.post("/ask")
def ask_question(body: InputBody):
    user_input = body.input.question
    print(f"USER INPUT: {user_input}")
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # CF deploy from ./srv places the file next to app.py; local runs may use parent folder.
    candidate_paths = [
        os.path.join(current_dir, "pu_chatbot.xlsx"),
        os.path.join(current_dir, "..", "pu_chatbot.xlsx"),
    ]
    file_path = next((path for path in candidate_paths if os.path.exists(path)), None)
    if file_path is None:
        raise HTTPException(status_code=500, detail="Training data file not found on server")

    dataframe = pu_bot.getDataFrame(file_path)
    if dataframe.empty:
        raise HTTPException(status_code=500, detail="Training data could not be loaded")

    answer = pu_bot.process_questions(user_input, dataframe)
    return {"answer": answer}


@app.get("/")
def root():
    return {"message": "Poornima University Chatbot API is running", "ask_route": "POST /ask"}

if __name__ == "__main__":
    import uvicorn
    PORT=int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)