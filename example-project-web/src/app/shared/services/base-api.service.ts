import {Injectable} from '@angular/core';
import {firstValueFrom} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {ZodSchema} from 'zod';

@Injectable({
  providedIn: 'root'
})
export class BaseApiService {
  constructor(private http: HttpClient) {
  }

  async get<T>(schema: ZodSchema, url: string, params?: any): Promise<T> {
    const obj = await firstValueFrom<T>(this.http.get<T>(url, {params}));
    if (schema) {
      schema.parse(obj);
    }
    return obj;
  }

  async post<T>(schema: ZodSchema, url: string, body: any): Promise<T> {
    const obj = await firstValueFrom<T>(this.http.post<T>(url, body));
    if (schema) {
      schema.parse(obj);
    }
    return obj;
  }

  async put<T>(schema: ZodSchema, url: string, body: any): Promise<T> {
    const obj = await firstValueFrom<T>(this.http.put<T>(url, body));
    if (schema) {
      schema.parse(obj);
    }
    return obj;
  }

  async patch<T>(schema: ZodSchema, url: string, body: any): Promise<T> {
    const obj = await firstValueFrom<T>(this.http.patch<T>(url, body));
    if (schema) {
      schema.parse(obj);
    }
    return obj;
  }

  async delete<T>(schema: ZodSchema, url: string): Promise<T> {
    const obj = await firstValueFrom<T>(this.http.delete<T>(url));
    if (schema) {
      schema.parse(obj);
    }
    return obj;
  }
}

