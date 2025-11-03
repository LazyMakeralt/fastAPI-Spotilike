import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { ActivatedRoute, Router, RouterLink } from '@angular/router'; 
import { Artist, Song } from '../../models/data.model'; 
import { ApiService } from '../../api'; 

@Component({
  selector: 'app-artist-detail',
  standalone: true, 
  imports: [CommonModule, RouterLink], 
  templateUrl: './artist-detail.html',
  styleUrls: ['./artist-detail.css']
})
export class ArtistDetailComponent implements OnInit {
  artist: Artist | undefined;
  songs: Song[] = [];
  artistId: number = 0;
  isLoading: boolean = true; 

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService
  ) { 
  }

  ngOnInit(): void {
    this.artistId = Number(this.route.snapshot.paramMap.get('id'));
    
    if (this.artistId) {
        this.loadArtistDetails(this.artistId);
        this.loadArtistSongs(this.artistId);
    }
  }

  loadArtistDetails(id: number): void {
    this.apiService.getArtistDetail(id).subscribe({
        next: (data) => {
            this.artist = data;
            this.isLoading = false;
        },
        error: () => {
            this.isLoading = false;
            this.artist = { 
                id: this.artistId, 
                name: `Artiste ID ${this.artistId} (Détails non chargés)`, 
                biography: "Erreur: Veuillez implémenter la route GET /api/artists/{id} dans votre backend pour afficher la biographie.", 
                avatar_url: "/assets/fuc.png" 
            };
        }
    });
  }

  loadArtistSongs(id: number): void {
    this.apiService.getArtistSongs(id).subscribe({
        next: (data) => this.songs = data,
        error: (err) => console.error("Erreur lors du chargement des morceaux :", err)
    });
  }

  formatDuration(seconds: number): string {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    const sec = remainingSeconds < 10 ? '0' + remainingSeconds : remainingSeconds;
    return `${minutes}:${sec}`;
  }
}
