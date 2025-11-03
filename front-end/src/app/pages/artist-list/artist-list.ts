import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { RouterLink } from '@angular/router'; 
import { ApiService } from '../../api'; 
import { Artist, Album } from '../../models/data.model'; 
import { forkJoin, of } from 'rxjs'; 
import { switchMap, map } from 'rxjs/operators';

@Component({
  selector: 'app-artist-list',
  standalone: true, 
  imports: [CommonModule, RouterLink], 
  templateUrl: './artist-list.html',
  styleUrls: ['./artist-list.css']
})
export class ArtistListComponent implements OnInit {
  artists: Artist[] = [];
  isLoading: boolean = true; 

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.loadArtistsData();
  }

  loadArtistsData(): void {
    this.isLoading = true;
    
    this.apiService.getAlbums().pipe(
      map((albums: Album[]) => {
        const artistIds = new Set<number>();
        albums.forEach(album => artistIds.add(album.artist_id));
        
        const detailCalls = Array.from(artistIds).map(artistId => 
          this.apiService.getArtistDetail(artistId)
        );
        return detailCalls;
      }),
      switchMap((detailCalls: any[]) => {
        if (detailCalls.length === 0) {
          return of([]); 
        }
        return forkJoin(detailCalls);
      })
    ).subscribe({
      next: (fullArtists: Artist[]) => {
        this.artists = fullArtists;
        this.isLoading = false;
      },
      error: (err) => {
        console.error("Erreur lors du chargement des artistes détaillés:", err);
        this.isLoading = false;
      }
    });
  }
  
}
