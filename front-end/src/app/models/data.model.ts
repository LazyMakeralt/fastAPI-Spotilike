
export interface Genre {
    id: number;
    title: string;
    description?: string;
}

export interface Song {
    id: number;
    title: string;
    duration: number; 
    artist_id: number;
    album_id: number;
    genres: Genre[];
}

export interface Album {
    id: number;
    title: string;
    release_date: string;
    cover_image_url?: string;
    artist_id: number;
    artist_name?: string; 
    songs: Song[];
}

export interface Artist {
    id: number;
    name: string;
    biography?: string;
    avatar_url?: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export interface UserCredentials {
    username?: string;
    email: string;
    password: string;
}