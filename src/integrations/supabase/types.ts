export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  public: {
    Tables: {
      calibration_data: {
        Row: {
          camera_id: number
          captured_images: Json[] | null
          created_at: string
          distortion_coeffs: Json | null
          id: string
          intrinsic_matrix: Json | null
          reprojection_error: number | null
          updated_at: string
        }
        Insert: {
          camera_id: number
          captured_images?: Json[] | null
          created_at?: string
          distortion_coeffs?: Json | null
          id?: string
          intrinsic_matrix?: Json | null
          reprojection_error?: number | null
          updated_at?: string
        }
        Update: {
          camera_id?: number
          captured_images?: Json[] | null
          created_at?: string
          distortion_coeffs?: Json | null
          id?: string
          intrinsic_matrix?: Json | null
          reprojection_error?: number | null
          updated_at?: string
        }
        Relationships: []
      }
      calibration_profiles: {
        Row: {
          cameras: Json
          created_at: string | null
          dartboard_registration: Json | null
          id: string
          is_active: boolean | null
          name: string
          scoring_parameters: Json | null
          updated_at: string | null
        }
        Insert: {
          cameras: Json
          created_at?: string | null
          dartboard_registration?: Json | null
          id?: string
          is_active?: boolean | null
          name: string
          scoring_parameters?: Json | null
          updated_at?: string | null
        }
        Update: {
          cameras?: Json
          created_at?: string | null
          dartboard_registration?: Json | null
          id?: string
          is_active?: boolean | null
          name?: string
          scoring_parameters?: Json | null
          updated_at?: string | null
        }
        Relationships: []
      }
      calls: {
        Row: {
          created_at: string | null
          ended_at: string | null
          id: string
          initiator_id: string
          recipient_id: string
          room_id: string
          started_at: string | null
          status: Database["public"]["Enums"]["call_status"]
          type: Database["public"]["Enums"]["call_type"]
          updated_at: string | null
        }
        Insert: {
          created_at?: string | null
          ended_at?: string | null
          id?: string
          initiator_id: string
          recipient_id: string
          room_id: string
          started_at?: string | null
          status?: Database["public"]["Enums"]["call_status"]
          type: Database["public"]["Enums"]["call_type"]
          updated_at?: string | null
        }
        Update: {
          created_at?: string | null
          ended_at?: string | null
          id?: string
          initiator_id?: string
          recipient_id?: string
          room_id?: string
          started_at?: string | null
          status?: Database["public"]["Enums"]["call_status"]
          type?: Database["public"]["Enums"]["call_type"]
          updated_at?: string | null
        }
        Relationships: []
      }
      camera_configs: {
        Row: {
          calibration_error: number | null
          calibration_images: number | null
          camera_index: number
          created_at: string | null
          distortion_coeffs: Json | null
          extrinsic_matrix: Json | null
          id: string
          intrinsic_matrix: Json | null
          name: string | null
          resolution: Json | null
          rvecs: Json | null
          status: Database["public"]["Enums"]["camera_status"] | null
          tvecs: Json | null
          updated_at: string | null
        }
        Insert: {
          calibration_error?: number | null
          calibration_images?: number | null
          camera_index: number
          created_at?: string | null
          distortion_coeffs?: Json | null
          extrinsic_matrix?: Json | null
          id?: string
          intrinsic_matrix?: Json | null
          name?: string | null
          resolution?: Json | null
          rvecs?: Json | null
          status?: Database["public"]["Enums"]["camera_status"] | null
          tvecs?: Json | null
          updated_at?: string | null
        }
        Update: {
          calibration_error?: number | null
          calibration_images?: number | null
          camera_index?: number
          created_at?: string | null
          distortion_coeffs?: Json | null
          extrinsic_matrix?: Json | null
          id?: string
          intrinsic_matrix?: Json | null
          name?: string | null
          resolution?: Json | null
          rvecs?: Json | null
          status?: Database["public"]["Enums"]["camera_status"] | null
          tvecs?: Json | null
          updated_at?: string | null
        }
        Relationships: []
      }
      camera_feeds: {
        Row: {
          camera_index: number
          device_id: string
          error_message: string | null
          id: number
          last_updated: string | null
          status: string
        }
        Insert: {
          camera_index: number
          device_id: string
          error_message?: string | null
          id?: number
          last_updated?: string | null
          status: string
        }
        Update: {
          camera_index?: number
          device_id?: string
          error_message?: string | null
          id?: number
          last_updated?: string | null
          status?: string
        }
        Relationships: []
      }
      chat_messages: {
        Row: {
          attachment_type: string | null
          attachment_url: string | null
          content: string
          created_at: string | null
          deleted_at: string | null
          drive_file_id: string | null
          drive_file_name: string | null
          drive_file_url: string | null
          edited_at: string | null
          id: string
          sender_id: string
        }
        Insert: {
          attachment_type?: string | null
          attachment_url?: string | null
          content: string
          created_at?: string | null
          deleted_at?: string | null
          drive_file_id?: string | null
          drive_file_name?: string | null
          drive_file_url?: string | null
          edited_at?: string | null
          id?: string
          sender_id: string
        }
        Update: {
          attachment_type?: string | null
          attachment_url?: string | null
          content?: string
          created_at?: string | null
          deleted_at?: string | null
          drive_file_id?: string | null
          drive_file_name?: string | null
          drive_file_url?: string | null
          edited_at?: string | null
          id?: string
          sender_id?: string
        }
        Relationships: []
      }
      file_uploads: {
        Row: {
          created_at: string | null
          file_path: string
          file_type: string
          filename: string
          id: string
          source: string
          updated_at: string | null
          user_id: string
        }
        Insert: {
          created_at?: string | null
          file_path: string
          file_type: string
          filename: string
          id?: string
          source?: string
          updated_at?: string | null
          user_id: string
        }
        Update: {
          created_at?: string | null
          file_path?: string
          file_type?: string
          filename?: string
          id?: string
          source?: string
          updated_at?: string | null
          user_id?: string
        }
        Relationships: []
      }
      github_issues: {
        Row: {
          action_items: string[] | null
          body: string | null
          created_at: string | null
          github_id: number
          id: string
          issue_number: number
          labels: string[] | null
          repository: string
          status: Database["public"]["Enums"]["issue_status"] | null
          summary: string | null
          title: string
          updated_at: string | null
          user_id: string | null
        }
        Insert: {
          action_items?: string[] | null
          body?: string | null
          created_at?: string | null
          github_id: number
          id?: string
          issue_number: number
          labels?: string[] | null
          repository: string
          status?: Database["public"]["Enums"]["issue_status"] | null
          summary?: string | null
          title: string
          updated_at?: string | null
          user_id?: string | null
        }
        Update: {
          action_items?: string[] | null
          body?: string | null
          created_at?: string | null
          github_id?: number
          id?: string
          issue_number?: number
          labels?: string[] | null
          repository?: string
          status?: Database["public"]["Enums"]["issue_status"] | null
          summary?: string | null
          title?: string
          updated_at?: string | null
          user_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "github_issues_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
        ]
      }
      google_drive_tokens: {
        Row: {
          access_token: string
          created_at: string
          expiry_date: string
          id: string
          refresh_token: string
          updated_at: string
          user_id: string
        }
        Insert: {
          access_token: string
          created_at?: string
          expiry_date: string
          id?: string
          refresh_token: string
          updated_at?: string
          user_id: string
        }
        Update: {
          access_token?: string
          created_at?: string
          expiry_date?: string
          id?: string
          refresh_token?: string
          updated_at?: string
          user_id?: string
        }
        Relationships: []
      }
      profiles: {
        Row: {
          avatar_url: string | null
          created_at: string
          id: string
          updated_at: string
          username: string | null
        }
        Insert: {
          avatar_url?: string | null
          created_at?: string
          id: string
          updated_at?: string
          username?: string | null
        }
        Update: {
          avatar_url?: string | null
          created_at?: string
          id?: string
          updated_at?: string
          username?: string | null
        }
        Relationships: []
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      call_status: "initiated" | "connected" | "ended" | "missed"
      call_type: "voice" | "video" | "screenshare"
      camera_status:
        | "disconnected"
        | "connected"
        | "calibrating"
        | "calibrated"
        | "error"
      file_source: "upload" | "drive"
      issue_status: "open" | "closed"
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type PublicSchema = Database[Extract<keyof Database, "public">]

export type Tables<
  PublicTableNameOrOptions extends
    | keyof (PublicSchema["Tables"] & PublicSchema["Views"])
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
        Database[PublicTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? (Database[PublicTableNameOrOptions["schema"]]["Tables"] &
      Database[PublicTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : PublicTableNameOrOptions extends keyof (PublicSchema["Tables"] &
        PublicSchema["Views"])
    ? (PublicSchema["Tables"] &
        PublicSchema["Views"])[PublicTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  PublicTableNameOrOptions extends
    | keyof PublicSchema["Tables"]
    | { schema: keyof Database },
  TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
  ? Database[PublicTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : PublicTableNameOrOptions extends keyof PublicSchema["Tables"]
    ? PublicSchema["Tables"][PublicTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  PublicEnumNameOrOptions extends
    | keyof PublicSchema["Enums"]
    | { schema: keyof Database },
  EnumName extends PublicEnumNameOrOptions extends { schema: keyof Database }
    ? keyof Database[PublicEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = PublicEnumNameOrOptions extends { schema: keyof Database }
  ? Database[PublicEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : PublicEnumNameOrOptions extends keyof PublicSchema["Enums"]
    ? PublicSchema["Enums"][PublicEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof PublicSchema["CompositeTypes"]
    | { schema: keyof Database },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof Database
  }
    ? keyof Database[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends { schema: keyof Database }
  ? Database[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof PublicSchema["CompositeTypes"]
    ? PublicSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never
