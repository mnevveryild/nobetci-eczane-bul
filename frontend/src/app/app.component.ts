import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { CITIES, CityData } from './cities-data';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  cities: CityData[] = CITIES;
  selectedIl: string = '';
  selectedIlce: string = '';
  email: string = '';
  loading: boolean = false;
  message: string = '';
  messageType: 'success' | 'error' | 'info' | '' = '';

  constructor(private http: HttpClient) {}

  get ilceler(): string[] {
    const city = this.cities.find(c => c.il === this.selectedIl);
    return city ? city.ilceler : [];
  }

  onIlChange() {
    this.selectedIlce = '';
  }

  submit() {
    if (!this.selectedIl || !this.selectedIlce || !this.email) {
      this.message = 'Lütfen tüm alanları doldurunuz.';
      this.messageType = 'error';
      return;
    }

    this.loading = true;
    this.message = 'Nöbetçi eczaneler bulunuyor ve e-posta gönderiliyor...';
    this.messageType = 'info';

    this.http.post<any>('http://localhost:8000/api/find-pharmacies', {
      il: this.selectedIl,
      ilce: this.selectedIlce,
      email: this.email
    }).subscribe({
      next: (res) => {
        this.loading = false;
        this.message = res.message || 'İşlem başarıyla tamamlandı.';
        this.messageType = 'success';
      },
      error: (err) => {
        this.loading = false;
        this.message = 'Hata oluştu: ' + (err.error?.detail || err.message);
        this.messageType = 'error';
      }
    });
  }
}
