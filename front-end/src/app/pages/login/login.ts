// src/app/pages/login/login.component.ts

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms'; // 👈 Formulaires réactifs
// ✅ CHEMINS CORRIGÉS
import { ApiService } from '../../api';
import { UserCredentials } from '../../models/data.model';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, RouterLink, ReactiveFormsModule], // 👈 Modules Formulaires
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class LoginComponent {
  loginForm: FormGroup;
  errorMessage: string = '';

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });
  }

  onSubmit() {
    this.errorMessage = '';
    if (this.loginForm.valid) {
      const credentials: UserCredentials = this.loginForm.value;
      
      this.apiService.login(credentials).subscribe({
        next: (response) => {
          localStorage.setItem('access_token', response.access_token);
          
          this.router.navigate(['/albums']); 
        },
        error: (err) => {
          this.errorMessage = 'Erreur de connexion. Vérifiez vos identifiants.';
          console.error('Login error:', err);
        }
      });
    } else {
      this.errorMessage = 'Veuillez remplir correctement tous les champs.';
    }
  }
}