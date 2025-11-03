import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { RouterLink } from '@angular/router'; 
import { Album, Artist } from '../../models/data.model'; 
import { ApiService } from '../../api'; 
import { forkJoin, of } from 'rxjs'; 
import { switchMap, map } from 'rxjs/operators';

@Component({
  selector: 'app-album-list',
  standalone: true, 
  imports: [CommonModule, RouterLink], 
  templateUrl: './album-list.html',
  styleUrls: ['./album-list.css']
})
export class AlbumListComponent implements OnInit {
  albums: Album[] = [];
  isLoading: boolean = true; 

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.loadAlbumsWithArtistNames();
  }

  loadAlbumsWithArtistNames(): void {
    this.isLoading = true;
    
    this.apiService.getAlbums().pipe(
      switchMap((albums: Album[]) => {
        this.albums = albums;
        
        const artistIds = new Set<number>();
        albums.forEach(album => artistIds.add(album.artist_id));
        
        const detailCalls = Array.from(artistIds).map(artistId => 
          this.apiService.getArtistDetail(artistId)
        );

        if (detailCalls.length === 0) {
          return of(new Map<number, Artist>());
        }

        return forkJoin(detailCalls).pipe(
          map((fullArtists: Artist[]) => {
            const artistMap = new Map<number, Artist>();
            fullArtists.forEach(artist => artistMap.set(artist.id, artist));
            return artistMap;
          })
        );
      })
    ).subscribe({
      next: (artistMap: Map<number, Artist>) => {
        this.albums = this.albums.map(album => {
          const artist = artistMap.get(album.artist_id);
          if (artist) {
            album.artist_name = artist.name; 
          }
          return album;
        });
        this.isLoading = false;
      },
      error: (err) => {
        console.error("Erreur critique lors du chargement des noms d'artistes:", err);
        this.isLoading = false;
            }
    });
  }
}