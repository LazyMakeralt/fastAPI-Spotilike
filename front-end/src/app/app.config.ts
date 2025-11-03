// src/app/app.config.ts

import { ApplicationConfig } from '@angular/core';
import { provideRouter, Routes } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';


// Pages principales
import { AlbumListComponent } from './pages/album-list/album-list';
import { AlbumDetailComponent } from './pages/album-detail/album-detail';
import { ArtistListComponent } from './pages/artist-list/artist-list';
import { ArtistDetailComponent } from './pages/artist-detail/artist-detail';

// Pages d'authentification
import { LoginComponent } from './pages/login/login';
import { RegisterComponent } from './pages/register/register';

import { authGuard } from './guards/auth.guard'; 

export const routes: Routes = [
 
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  
  { path: '', redirectTo: '/albums', pathMatch: 'full' }, 
  
  { 
    path: 'albums', 
    component: AlbumListComponent,
    canActivate: [authGuard] 
  },
  { 
    path: 'albums/:id', 
    component: AlbumDetailComponent,
    canActivate: [authGuard] 
  },
  { 
    path: 'artists', 
    component: ArtistListComponent,
    canActivate: [authGuard] 
  },
  { 
    path: 'artists/:id', 
    component: ArtistDetailComponent,
    canActivate: [authGuard] 
  },
  
  { path: '**', redirectTo: '/albums' } 
];

// ----------------------------------------------------------------------
// CONFIGURATION GLOBALE
// ----------------------------------------------------------------------
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    // Activation du client HTTP
    provideHttpClient() 
  ]
};