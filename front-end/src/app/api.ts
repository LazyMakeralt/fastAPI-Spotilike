// src/app/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Artist, Album, Song, AuthResponse, UserCredentials } from './models/data.model'; 

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:8000/api'; 

  constructor(private http: HttpClient) { }


  login(credentials: UserCredentials): Observable<AuthResponse> {

       const loginData = {
           username: credentials.email,
           password: credentials.password
       };


      return this.http.post<AuthResponse>(`${this.apiUrl}/users/login`, loginData);
  }


  register(credentials: UserCredentials): Observable<any> {
      return this.http.post<any>(`${this.apiUrl}/users/signup`, credentials); 
  }
  


  getToken(): string | null {
      return localStorage.getItem('access_token');
  }


  private getAuthHeaders(): HttpHeaders {
      const token = this.getToken();
      if (token) {
          return new HttpHeaders({
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
          });
      }
      return new HttpHeaders({
          'Content-Type': 'application/json'
      });
  }

  getAlbums(): Observable<Album[]> {
    return this.http.get<Album[]>(`${this.apiUrl}/albums`);
  }

  getAlbumDetail(id: number): Observable<Album> {
    return this.http.get<Album>(`${this.apiUrl}/albums/${id}`);
  }

  getArtistDetail(id: number): Observable<Artist> {
    return this.http.get<Artist>(`${this.apiUrl}/artists/${id}`); 
  }


  getArtistSongs(id: number): Observable<Song[]> {
    return this.http.get<Song[]>(`${this.apiUrl}/artists/${id}/songs`);
  }

  deleteAlbum(id: number): Observable<any> {
      return this.http.delete<any>(`${this.apiUrl}/albums/${id}`, { headers: this.getAuthHeaders() });
  }
}
