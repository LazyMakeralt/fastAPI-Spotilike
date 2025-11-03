// src/app/pages/register/register.component.ts

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms'; 
// ✅ CHEMINS CORRIGÉS
import { ApiService } from '../../api';
import { UserCredentials } from '../../models/data.model';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, RouterLink, ReactiveFormsModule], 
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class RegisterComponent {
  registerForm: FormGroup;
  errorMessage: string = '';
  successMessage: string = '';

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private router: Router
  ) {
    this.registerForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required]
    }, { validators: this.passwordMatchValidator });
  }

  // Validateur personnalisé pour vérifier que les mots de passe correspondent
  passwordMatchValidator(form: FormGroup) {
    return form.get('password')?.value === form.get('confirmPassword')?.value
      ? null : { mismatch: true };
  }

  onSubmit() {
    this.errorMessage = '';
    this.successMessage = '';

    if (this.registerForm.valid) {
      const { email, password, username } = this.registerForm.value;
      const credentials: UserCredentials = { email, password, username };
      
      this.apiService.register(credentials).subscribe({
        next: (response) => {
          this.successMessage = 'Inscription réussie ! Vous pouvez maintenant vous connecter.';
          // Optionnel: Réinitialiser le formulaire
          this.registerForm.reset(); 
          // Redirection après un délai
          setTimeout(() => this.router.navigate(['/login']), 2000);
        },
        error: (err) => {
          this.errorMessage = 'Erreur lors de l\'inscription. L\'utilisateur existe peut-être déjà.';
          console.error('Register error:', err);
        }
      });
    } else {
      this.errorMessage = 'Veuillez remplir correctement tous les champs.';
    }
  }
}