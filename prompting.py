#%%
# write prompt for LLM to generate answer from retrived data

SYSTEM_PROMPT = """
You are an expert in financial regulations.
Only answer from the provided context.
If the answer is not present, say that the information is unavailable.
Never hallucinate.
Always provide:

1. Executive summary in simple language

2. Technical explanation

3. Evidence: Always provide Document name and page numbers. Provide sections and paragraph if available.

4. Confidence (Low/Medium/High): Based on the infomration present in the context.

Write your answer in a structured JSON format:

{
  "executive_summary": "...",
  "technical_explanation": "...",
  "citations": [
    "Document 1, page 10",
    "Document 4, page 34, section III"
  ],

  "confidence": "High"
}
"""

def user_prompt(retrieved_chunks, query):

    context = ''
    
    for chunk in retrieved_chunks:
        context += f'''Chunk ID: {chunk['chunk_id']}
        Document name: {chunk['document_name']}
        Page numbers: {chunk['page_numbers']}
        Text: {chunk['text']}
        '''

    prompt = f'''Context:
    {context}
    Question: {query}
    '''
    return prompt

