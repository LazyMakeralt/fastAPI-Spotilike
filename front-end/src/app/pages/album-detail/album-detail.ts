// src/app/pages/album-detail/album-detail.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { ActivatedRoute, Router, RouterLink } from '@angular/router'; 
import { Album } from '../../models/data.model'; 
import { ApiService } from '../../api'; 

@Component({
  selector: 'app-album-detail',
  standalone: true, 
  imports: [CommonModule, RouterLink], 
  templateUrl: './album-detail.html', 
  styleUrls: ['./album-detail.css']
})
export class AlbumDetailComponent implements OnInit {
  album: Album | undefined; 
  albumId: number = 0;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService
  ) { }

  ngOnInit(): void {
    this.albumId = Number(this.route.snapshot.paramMap.get('id'));
    
    this.apiService.getAlbumDetail(this.albumId).subscribe({
      next: (data) => this.album = data,
      error: () => this.router.navigate(['/albums']) 
    });
  }

  formatDuration(seconds: number): string {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    const sec = remainingSeconds < 10 ? '0' + remainingSeconds : remainingSeconds;
    return `${minutes}:${sec}`;
  }
}