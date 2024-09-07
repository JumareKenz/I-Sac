import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ChatbotService {
  private rasaUrl = 'http://localhost:5005/webhooks/rest/webhook';

  constructor(private http: HttpClient) {}

  sendMessage(message: string): Observable<any[]> {
    const payload = {
      sender: 'user',
      message: message,
    };
    return this.http.post<any[]>(this.rasaUrl, payload);
  }
}
