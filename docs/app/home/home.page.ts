import { Component, OnInit, ViewChild } from '@angular/core';
import { ChatbotService } from '../services/isac.service';
import { IonContent } from '@ionic/angular';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {
  userMessage: string = '';
  messages: { sender: string; text: string }[] = [];
  isTyping: boolean = false;

  @ViewChild(IonContent) content!: IonContent;

  constructor(private chatbotService: ChatbotService) {}

  ngOnInit() {
    // Any initialization logic can go here
  }

  // Function to send a message
  sendMessage() {
    if (this.userMessage.trim() !== '') {
      // Add user's message to the chat
      this.messages.push({ text: this.userMessage, sender: 'user' });
      const userMessage = this.userMessage; // Save the user's message
      this.userMessage = '';

      // Scroll to bottom immediately after sending the user's message
      this.scrollToBottom();

      // Simulate bot typing
      this.isTyping = true;

      // Send message to Rasa bot via the service
      this.chatbotService.sendMessage(userMessage).subscribe(
        (response) => {
          this.isTyping = false;

          // Rasa can return multiple messages, so we loop through them
          response.forEach((res) => {
            console.log(`Received response:`, res);
            this.messages.push({ text: res.text, sender: 'bot' });

            // Extract URL from the response text if it looks like a URL
            const url = this.extractUrl(res.text);
            if (url) {
              this.openPDF(url);
            }
          });

          // Scroll to the bottom after receiving the response
          this.scrollToBottom();
        },
        (error) => {
          this.isTyping = false;
          console.error('Error getting bot response:', error);
          this.messages.push({
            text: "I'm sorry, can't connect to the server, please try again later.",
            sender: 'bot',
          });

          // Scroll to the bottom after handling the error
          this.scrollToBottom();
        }
      );
    }
  }

  // Helper method to extract URL from response text
  extractUrl(text: string): string | null {
    // Regular expression to match URLs
    const urlRegex = /https?:\/\/[^\s]+/;
    const matches = text.match(urlRegex);
    return matches ? matches[0] : null;
  }

  // Function to open the PDF in a new window or within the app
  openPDF(text: string) {
    const url = this.extractUrl(text);
    if (url) {
      console.log(`Attempting to open PDF at: ${url}`);
      window.open(url, '_blank');
    } else {
      console.error('No valid URL found in the text:', text);
    }
  }

  // Unified function to handle button click
  handleButtonClick(text: string) {
    this.openPDF(text);
  }

  // Function to scroll to the bottom of the chat
  scrollToBottom() {
    setTimeout(() => {
      this.content.scrollToBottom(300).then(() => {
        console.log('Scrolled to bottom');
      }).catch(err => {
        console.error('Error scrolling to bottom', err);
      });
    }, 100); // Adjust the timeout if necessary
  }

  // Method to refresh chat
  refresh() {
    this.messages = [];
    this.userMessage = '';
    this.isTyping = false;
    this.scrollToBottom(); // Optional, may not be necessary if messages are cleared
  }

  // Method to navigate to the portal
  portal() {
    window.open('https://www.portal.abu.edu.ng', '_blank');
  }

  website() {
    window.open('https://www.abu.edu.ng', '_blank');
  }
}
