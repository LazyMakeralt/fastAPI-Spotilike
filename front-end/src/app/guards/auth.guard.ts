
import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { ApiService } from '../api'; 

export const authGuard: CanActivateFn = () => {
  const apiService = inject(ApiService);
  const router = inject(Router);
  
  // 1. Vérifie si le jeton existe dans le localStorage
  const token = apiService.getToken();

  if (token) {
    // 2. Si un jeton est présent, l'accès est autorisé
    return true;
  } else {
    // 3. Si aucun jeton n'est présent, redirige vers la page de connexion
    return router.createUrlTree(['/login']);
  }
};