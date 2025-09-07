import time
import re
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
import google.generativeai as genai
from src.search import SearchEngine, WebScraper

# Global socketio instance will be set by main app
socketio = None

def set_socketio(socketio_instance):
    global socketio
    socketio = socketio_instance

class ResearchAgent:
    def __init__(self, task_id):
        self.task_id = task_id
        self.status = 'initialized'
        self.thoughts = []
        self.report = ''
        self.progress = 0
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise Exception("GEMINI_API_KEY environment variable not found.")
            print(f"Found Gemini API Key starting with: {api_key[:4]}...") # Debug print
            genai.configure(api_key=api_key)
            self.genai_model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            raise Exception("Failed to configure Gemini API. Make sure you have GEMINI_API_KEY set.")
        self.search_engine = SearchEngine()
        self.web_scraper = WebScraper()
        
    def add_thought(self, thought):
        """Add a thought and emit it via WebSocket"""
        self.thoughts.append(thought)
        print(f"[Agent {self.task_id}] {thought}")
        # Emit to WebSocket room for this task
        if socketio:
            socketio.emit('thought', {'thought': thought, 'task_id': self.task_id}, room=self.task_id)
        
    def update_progress(self, progress):
        """Update progress and emit it via WebSocket"""
        self.progress = progress
        if socketio:
            socketio.emit('progress', {'progress': progress, 'task_id': self.task_id}, room=self.task_id)
        
    def research(self, query):
        """Main research method"""
        try:
            self.status = 'running'
            self.add_thought(f"Starting research on: {query}")
            
            # Step 1: Break down the query into sub-questions
            self.add_thought("Breaking down the query into sub-questions...")
            sub_questions = self.break_down_query(query)
            self.update_progress(10)
            
            # Step 2: Research each sub-question
            all_findings = []
            for i, sub_question in enumerate(sub_questions):
                self.add_thought(f"Researching: {sub_question}")
                findings = self.research_sub_question(sub_question)
                all_findings.extend(findings)
                progress = 10 + (70 * (i + 1) / len(sub_questions))
                self.update_progress(int(progress))
                
            # Step 3: Compile final report
            self.add_thought("Compiling final report...")
            self.report = self.compile_report(query, sub_questions, all_findings)
            self.update_progress(100)
            
            self.status = 'completed'
            self.add_thought("Research completed successfully!")
            
            # Emit final report
            if socketio:
                socketio.emit('report_complete', {
                    'task_id': self.task_id,
                    'report': self.report
                }, room=self.task_id)
            
        except Exception as e:
            self.status = 'error'
            self.add_thought(f"Error occurred: {str(e)}")
            if socketio:
                socketio.emit('error', {'task_id': self.task_id, 'error': str(e)}, room=self.task_id)
    
    def break_down_query(self, query):
        """Break down the main query into sub-questions using OpenAI"""
        try:
            prompt = f"""
            Break down this research query into 3-5 specific sub-questions that would help gather comprehensive information:
            
            Query: {query}
            
            Return only the sub-questions, one per line, without numbering or bullet points.
            """
            
            response = self.genai_model.generate_content(prompt)
            
            sub_questions = [q.strip() for q in response.text.strip().split('\n') if q.strip()]
            
            for i, question in enumerate(sub_questions, 1):
                self.add_thought(f"Sub-question {i}: {question}")
                
            return sub_questions
            
        except Exception as e:
            if 'quota' in str(e).lower():
                raise Exception("Gemini API quota exceeded. Please check your plan and billing details.")
            self.add_thought(f"Error breaking down query: {str(e)}")
            # Fallback to basic sub-questions
            return [
                f"What are the key players in {query}?",
                f"What are the recent trends in {query}?",
                f"What are the main challenges in {query}?"
            ]
    
    def research_sub_question(self, sub_question):
        """Research a single sub-question"""
        findings = []
        
        try:
            # Perform real search
            self.add_thought(f"Searching for: {sub_question}")
            search_results = self.search_engine.search(sub_question, num_results=3)
            
            if not search_results:
                self.add_thought("No search results found, using fallback data")
                return [{
                    'source': 'Fallback Data',
                    'url': 'N/A',
                    'summary': f"Unable to find specific information about: {sub_question}. This would typically contain relevant market data, industry insights, and expert analysis."
                }]
            
            # Scrape top results
            for i, result in enumerate(search_results, 1):
                self.add_thought(f"Scraping result {i}: {result['title']}")
                
                # Scrape the webpage
                scraped_content = self.web_scraper.scrape_url(result['url'])
                
                if scraped_content and len(scraped_content) > 100:
                    # Summarize the scraped content
                    summary = self.summarize_content(scraped_content, sub_question)
                    findings.append({
                        'source': result['title'],
                        'url': result['url'],
                        'summary': summary
                    })
                else:
                    # Use the search snippet if scraping failed
                    self.add_thought(f"Scraping failed for {result['title']}, using search snippet")
                    findings.append({
                        'source': result['title'],
                        'url': result['url'],
                        'summary': result.get('snippet', 'No content available')
                    })
                    
        except Exception as e:
            self.add_thought(f"Error researching sub-question: {str(e)}")
            # Provide fallback finding
            findings.append({
                'source': 'Error Recovery',
                'url': 'N/A',
                'summary': f"Research encountered an error for: {sub_question}. This would typically include relevant information from industry sources and expert analysis."
            })
            
        return findings
    
    def summarize_content(self, content, context):
        """Summarize scraped content using OpenAI"""
        try:
            prompt = f"""
            Summarize the following content in the context of this research question: {context}
            
            Content: {content[:2000]}  # Limit content length
            
            Provide a concise summary focusing on the most relevant information for the research question.
            """
            
            response = self.genai_model.generate_content(prompt)
            
            return response.text.strip()
            
        except Exception as e:
            if 'quota' in str(e).lower():
                return "Summary unavailable due to API quota exceeded."
            self.add_thought(f"Error summarizing content: {str(e)}")
            return "Summary unavailable due to processing error."
    
    def compile_report(self, original_query, sub_questions, findings):
        """Compile all findings into a structured report"""
        try:
            # Prepare findings text
            findings_text = ""
            for finding in findings:
                findings_text += f"Source: {finding['source']}\n"
                findings_text += f"Summary: {finding['summary']}\n\n"
            
            prompt = f"""
            You are a professional business analyst and research expert. Your task is to generate a comprehensive, client-ready report based on the provided research findings. The report should be well-structured, insightful, and written in a formal, business-oriented tone.

            **Client's Original Request:** "{original_query}"

            **Key Research Questions Explored:**
            {chr(10).join([f"- {q}" for q in sub_questions])}

            **Synthesized Research Findings:**
            {findings_text}

            ---

            **Report Generation Instructions:**

            Please generate a final report with the following sections. Ensure each section is clearly titled and contains insightful analysis, not just a list of facts. Use Markdown for professional formatting.

            1.  **Executive Summary:**
                *   Start with a concise, high-level overview of the key findings and conclusions. This should be a standalone summary that gives a busy executive everything they need to know.

            2.  **Introduction:**
                *   Briefly introduce the topic and the scope of the research based on the original query.

            3.  **Key Findings & Analysis:**
                *   Present the most critical insights discovered during the research.
                *   Organize these findings into logical themes or categories.
                *   Use bullet points for clarity and impact.
                *   **Crucially, do not just repeat the summaries.** Synthesize the information to draw meaningful connections and conclusions.

            4.  **Market Trends & Future Outlook (if applicable):**
                *   Analyze the current market landscape and project future trends.
                *   Discuss potential opportunities, challenges, and disruptive factors.

            5.  **Conclusion & Strategic Recommendations:**
                *   Summarize the research and reiterate the most important takeaways.
                *   Provide clear, actionable recommendations based on the findings. What should the client do next with this information?

            6.  **Sources & Further Reading:**
                *   List the primary sources used for the research to ensure credibility.

            **Formatting Guidelines:**
            *   Use Markdown for headings (`##`), bolding (`**text**`), and bullet points (`*`).
            *   Maintain a professional and objective tone throughout the report.
            *   Ensure the report is well-organized, easy to read, and free of jargon where possible.

            Now, please generate the complete, professional report.
            """
            
            response = self.genai_model.generate_content(prompt)
            
            return response.text.strip()
            
        except Exception as e:
            if 'quota' in str(e).lower():
                return "Report compilation failed. API quota exceeded. Please check your plan and billing details."
            self.add_thought(f"Error compiling report: {str(e)}")
            return "Report compilation failed due to processing error."

