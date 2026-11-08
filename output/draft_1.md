# Introduction to RAG: Teaching AI to Look Things Up

**For:** Class 12 students | **Time:** 20 minutes | **Level:** Beginner

## What you will learn
- What RAG means
- Why AI sometimes gives wrong answers
- The 4 steps of RAG
- Where RAG is used

## 1. The problem: AI can guess wrong
You may have used an AI chatbot like ChatGPT. It writes well and answers fast. But it has two problems.

First, it only knows what it learned during training. It may not know new things. For example, it may not know this year's exam dates.

Second, it may make up an answer when it does not know. This is called a hallucination. The answer sounds right, but it is wrong.

## 2. What is RAG?
RAG stands for Retrieval-Augmented Generation. The name has three important words.
- **Retrieval:** finding useful information.
- **Augmented:** adding to something. Here, we add the found information to the question.
- **Generation:** the AI writes the answer.

So RAG means this: first find the right information. Then let the AI write the answer using it.

Think of two kinds of exams. In a closed-book exam, you answer from memory only. In an open-book exam, you can look in your book. RAG lets the AI take an open-book exam.

## 3. How RAG works: 4 steps
Imagine a college in Hyderabad has a PDF with all its rules. A student asks: "What is the last date to pay the fee?"

**Step 1: Prepare the documents.** The PDF is cut into small pieces. These pieces are called chunks. Each chunk is a few lines long.

**Step 2: Make them searchable.** Each chunk is changed into a list of numbers. This list is called an embedding. It captures the meaning of the text. Chunks with similar meaning get similar numbers. The numbers are saved in a vector database.

**Step 3: Retrieve.** The question is also changed into numbers. The system finds the chunks closest in meaning to the question. Say it finds this chunk: "The last date to pay the fee is 30 June."

**Step 4: Generate.** The system gives the AI the question and the chunk together. The AI reads the chunk and writes: "The last date to pay the fee is 30 June."

The AI did not need to learn the PDF in advance. It just looked the answer up.

## 4. Why RAG is useful
- **Fresh information:** change the documents, and the answers change. There is no need to train the AI again.
- **Fewer wrong answers:** the AI uses real text, so it guesses less.
- **Proof:** the system can show which document the answer came from.
- **Private data:** a school can use its own documents.

## 5. Where is RAG used?
- A bank chatbot that answers from the bank's own rules.
- A study app that answers questions from NCERT textbooks.
- A company help desk that reads old support tickets.

## 6. Limits of RAG
RAG is not perfect. If the search finds the wrong chunk, the answer will be wrong. If the documents have mistakes, the answer will have mistakes. So RAG gives fewer wrong answers, but it does not remove them all.

## 7. Key words
| Word | Simple meaning |
|---|---|
| LLM | An AI that reads and writes text, like ChatGPT |
| Hallucination | A wrong answer that sounds right |
| Chunk | A small piece of a document |
| Embedding | A list of numbers that shows the meaning of text |
| Vector database | A place where embeddings are saved and searched |

## 8. Check yourself
**Q1.** What does the "R" in RAG stand for?
**Answer:** Retrieval, which means finding useful information.

**Q2.** In the open-book exam example, what is the "book"?
**Answer:** The documents, such as the college PDF.

**Q3.** What is an embedding?
**Answer:** A list of numbers that shows the meaning of a piece of text.

**Q4.** True or false: when the documents change, we must train the AI again.
**Answer:** False. We only update the documents.

**Q5.** Why can RAG still give a wrong answer?
**Answer:** The search may find the wrong chunk, or the document may have a mistake.

## Summary
RAG helps AI look things up before it answers. First it retrieves the right information. Then it writes the answer from that information. This gives fresher and more trusted answers.
