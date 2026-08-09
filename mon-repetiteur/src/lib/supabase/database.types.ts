export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  graphql_public: {
    Tables: {
      [_ in never]: never
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      graphql: {
        Args: {
          extensions?: Json
          operationName?: string
          query?: string
          variables?: Json
        }
        Returns: Json
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
  public: {
    Tables: {
      ai_conversations: {
        Row: {
          context: Json
          ended_at: string | null
          id: string
          profile_id: string
          started_at: string
        }
        Insert: {
          context?: Json
          ended_at?: string | null
          id?: string
          profile_id: string
          started_at?: string
        }
        Update: {
          context?: Json
          ended_at?: string | null
          id?: string
          profile_id?: string
          started_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "ai_conversations_profile_id_fkey"
            columns: ["profile_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
        ]
      }
      ai_messages: {
        Row: {
          content: string
          conversation_id: string
          created_at: string
          id: string
          role: Database["public"]["Enums"]["ai_message_role"]
        }
        Insert: {
          content: string
          conversation_id: string
          created_at?: string
          id?: string
          role: Database["public"]["Enums"]["ai_message_role"]
        }
        Update: {
          content?: string
          conversation_id?: string
          created_at?: string
          id?: string
          role?: Database["public"]["Enums"]["ai_message_role"]
        }
        Relationships: [
          {
            foreignKeyName: "ai_messages_conversation_id_fkey"
            columns: ["conversation_id"]
            isOneToOne: false
            referencedRelation: "ai_conversations"
            referencedColumns: ["id"]
          },
        ]
      }
      attempts: {
        Row: {
          answer: Json
          attemptable_id: string
          attemptable_type: Database["public"]["Enums"]["attemptable_type"]
          attempted_at: string
          id: string
          is_correct: boolean | null
          profile_id: string
          score: number | null
        }
        Insert: {
          answer: Json
          attemptable_id: string
          attemptable_type: Database["public"]["Enums"]["attemptable_type"]
          attempted_at?: string
          id?: string
          is_correct?: boolean | null
          profile_id: string
          score?: number | null
        }
        Update: {
          answer?: Json
          attemptable_id?: string
          attemptable_type?: Database["public"]["Enums"]["attemptable_type"]
          attempted_at?: string
          id?: string
          is_correct?: boolean | null
          profile_id?: string
          score?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "attempts_profile_id_fkey"
            columns: ["profile_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
        ]
      }
      classes: {
        Row: {
          code: string
          id: string
          name: string
          order: number
          program_id: string
        }
        Insert: {
          code: string
          id?: string
          name: string
          order?: number
          program_id: string
        }
        Update: {
          code?: string
          id?: string
          name?: string
          order?: number
          program_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "classes_program_id_fkey"
            columns: ["program_id"]
            isOneToOne: false
            referencedRelation: "programs"
            referencedColumns: ["id"]
          },
        ]
      }
      exam_questions: {
        Row: {
          exam_id: string
          exercise_id: string
          id: string
          order: number
        }
        Insert: {
          exam_id: string
          exercise_id: string
          id?: string
          order?: number
        }
        Update: {
          exam_id?: string
          exercise_id?: string
          id?: string
          order?: number
        }
        Relationships: [
          {
            foreignKeyName: "exam_questions_exam_id_fkey"
            columns: ["exam_id"]
            isOneToOne: false
            referencedRelation: "exams"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "exam_questions_exercise_id_fkey"
            columns: ["exercise_id"]
            isOneToOne: false
            referencedRelation: "exercises"
            referencedColumns: ["id"]
          },
        ]
      }
      exams: {
        Row: {
          created_at: string
          created_by: string | null
          id: string
          permission_reference: string | null
          program_id: string
          rights_status: Database["public"]["Enums"]["exam_rights_status"]
          session: string | null
          source: string | null
          source_url: string | null
          status: Database["public"]["Enums"]["content_status"]
          subject_id: string
          title: string
          updated_at: string
          year: number
        }
        Insert: {
          created_at?: string
          created_by?: string | null
          id?: string
          permission_reference?: string | null
          program_id: string
          rights_status?: Database["public"]["Enums"]["exam_rights_status"]
          session?: string | null
          source?: string | null
          source_url?: string | null
          status?: Database["public"]["Enums"]["content_status"]
          subject_id: string
          title: string
          updated_at?: string
          year: number
        }
        Update: {
          created_at?: string
          created_by?: string | null
          id?: string
          permission_reference?: string | null
          program_id?: string
          rights_status?: Database["public"]["Enums"]["exam_rights_status"]
          session?: string | null
          source?: string | null
          source_url?: string | null
          status?: Database["public"]["Enums"]["content_status"]
          subject_id?: string
          title?: string
          updated_at?: string
          year?: number
        }
        Relationships: [
          {
            foreignKeyName: "exams_created_by_fkey"
            columns: ["created_by"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "exams_program_id_fkey"
            columns: ["program_id"]
            isOneToOne: false
            referencedRelation: "programs"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "exams_subject_id_fkey"
            columns: ["subject_id"]
            isOneToOne: false
            referencedRelation: "subjects"
            referencedColumns: ["id"]
          },
        ]
      }
      exercises: {
        Row: {
          content: Json
          created_at: string
          created_by: string | null
          difficulty: Database["public"]["Enums"]["difficulty_level"]
          id: string
          prompt: string
          skill_id: string
          status: Database["public"]["Enums"]["content_status"]
          type: Database["public"]["Enums"]["exercise_type"]
          updated_at: string
        }
        Insert: {
          content: Json
          created_at?: string
          created_by?: string | null
          difficulty?: Database["public"]["Enums"]["difficulty_level"]
          id?: string
          prompt: string
          skill_id: string
          status?: Database["public"]["Enums"]["content_status"]
          type: Database["public"]["Enums"]["exercise_type"]
          updated_at?: string
        }
        Update: {
          content?: Json
          created_at?: string
          created_by?: string | null
          difficulty?: Database["public"]["Enums"]["difficulty_level"]
          id?: string
          prompt?: string
          skill_id?: string
          status?: Database["public"]["Enums"]["content_status"]
          type?: Database["public"]["Enums"]["exercise_type"]
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "exercises_created_by_fkey"
            columns: ["created_by"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "exercises_skill_id_fkey"
            columns: ["skill_id"]
            isOneToOne: false
            referencedRelation: "skills"
            referencedColumns: ["id"]
          },
        ]
      }
      lessons: {
        Row: {
          content: string
          created_at: string
          created_by: string | null
          id: string
          published_at: string | null
          skill_id: string
          status: Database["public"]["Enums"]["content_status"]
          title: string
          updated_at: string
        }
        Insert: {
          content: string
          created_at?: string
          created_by?: string | null
          id?: string
          published_at?: string | null
          skill_id: string
          status?: Database["public"]["Enums"]["content_status"]
          title: string
          updated_at?: string
        }
        Update: {
          content?: string
          created_at?: string
          created_by?: string | null
          id?: string
          published_at?: string | null
          skill_id?: string
          status?: Database["public"]["Enums"]["content_status"]
          title?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "lessons_created_by_fkey"
            columns: ["created_by"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "lessons_skill_id_fkey"
            columns: ["skill_id"]
            isOneToOne: false
            referencedRelation: "skills"
            referencedColumns: ["id"]
          },
        ]
      }
      mock_exam_answers: {
        Row: {
          answer: Json
          id: string
          is_correct: boolean | null
          mock_exam_id: string
          mock_exam_question_id: string
        }
        Insert: {
          answer: Json
          id?: string
          is_correct?: boolean | null
          mock_exam_id: string
          mock_exam_question_id: string
        }
        Update: {
          answer?: Json
          id?: string
          is_correct?: boolean | null
          mock_exam_id?: string
          mock_exam_question_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "mock_exam_answers_mock_exam_id_fkey"
            columns: ["mock_exam_id"]
            isOneToOne: false
            referencedRelation: "mock_exams"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "mock_exam_answers_mock_exam_question_id_fkey"
            columns: ["mock_exam_question_id"]
            isOneToOne: true
            referencedRelation: "mock_exam_questions"
            referencedColumns: ["id"]
          },
        ]
      }
      mock_exam_questions: {
        Row: {
          exercise_id: string
          id: string
          mock_exam_id: string
          order: number
        }
        Insert: {
          exercise_id: string
          id?: string
          mock_exam_id: string
          order?: number
        }
        Update: {
          exercise_id?: string
          id?: string
          mock_exam_id?: string
          order?: number
        }
        Relationships: [
          {
            foreignKeyName: "mock_exam_questions_exercise_id_fkey"
            columns: ["exercise_id"]
            isOneToOne: false
            referencedRelation: "exercises"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "mock_exam_questions_mock_exam_id_fkey"
            columns: ["mock_exam_id"]
            isOneToOne: false
            referencedRelation: "mock_exams"
            referencedColumns: ["id"]
          },
        ]
      }
      mock_exams: {
        Row: {
          class_id: string
          id: string
          profile_id: string
          score: number | null
          started_at: string
          status: Database["public"]["Enums"]["mock_exam_status"]
          subject_id: string
          submitted_at: string | null
        }
        Insert: {
          class_id: string
          id?: string
          profile_id: string
          score?: number | null
          started_at?: string
          status?: Database["public"]["Enums"]["mock_exam_status"]
          subject_id: string
          submitted_at?: string | null
        }
        Update: {
          class_id?: string
          id?: string
          profile_id?: string
          score?: number | null
          started_at?: string
          status?: Database["public"]["Enums"]["mock_exam_status"]
          subject_id?: string
          submitted_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "mock_exams_class_id_fkey"
            columns: ["class_id"]
            isOneToOne: false
            referencedRelation: "classes"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "mock_exams_profile_id_fkey"
            columns: ["profile_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "mock_exams_subject_id_fkey"
            columns: ["subject_id"]
            isOneToOne: false
            referencedRelation: "subjects"
            referencedColumns: ["id"]
          },
        ]
      }
      profiles: {
        Row: {
          created_at: string
          full_name: string | null
          id: string
          role: Database["public"]["Enums"]["user_role"]
          updated_at: string
        }
        Insert: {
          created_at?: string
          full_name?: string | null
          id: string
          role?: Database["public"]["Enums"]["user_role"]
          updated_at?: string
        }
        Update: {
          created_at?: string
          full_name?: string | null
          id?: string
          role?: Database["public"]["Enums"]["user_role"]
          updated_at?: string
        }
        Relationships: []
      }
      programs: {
        Row: {
          code: string
          created_at: string
          id: string
          language: string
          name: string
        }
        Insert: {
          code: string
          created_at?: string
          id?: string
          language: string
          name: string
        }
        Update: {
          code?: string
          created_at?: string
          id?: string
          language?: string
          name?: string
        }
        Relationships: []
      }
      skill_progress: {
        Row: {
          id: string
          mastery_score: number
          profile_id: string
          skill_id: string
          updated_at: string
        }
        Insert: {
          id?: string
          mastery_score?: number
          profile_id: string
          skill_id: string
          updated_at?: string
        }
        Update: {
          id?: string
          mastery_score?: number
          profile_id?: string
          skill_id?: string
          updated_at?: string
        }
        Relationships: [
          {
            foreignKeyName: "skill_progress_profile_id_fkey"
            columns: ["profile_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "skill_progress_skill_id_fkey"
            columns: ["skill_id"]
            isOneToOne: false
            referencedRelation: "skills"
            referencedColumns: ["id"]
          },
        ]
      }
      skills: {
        Row: {
          id: string
          order: number
          title: string
          topic_id: string
        }
        Insert: {
          id?: string
          order?: number
          title: string
          topic_id: string
        }
        Update: {
          id?: string
          order?: number
          title?: string
          topic_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "skills_topic_id_fkey"
            columns: ["topic_id"]
            isOneToOne: false
            referencedRelation: "topics"
            referencedColumns: ["id"]
          },
        ]
      }
      study_plans: {
        Row: {
          created_at: string
          id: string
          profile_id: string
          status: Database["public"]["Enums"]["study_plan_status"]
        }
        Insert: {
          created_at?: string
          id?: string
          profile_id: string
          status?: Database["public"]["Enums"]["study_plan_status"]
        }
        Update: {
          created_at?: string
          id?: string
          profile_id?: string
          status?: Database["public"]["Enums"]["study_plan_status"]
        }
        Relationships: [
          {
            foreignKeyName: "study_plans_profile_id_fkey"
            columns: ["profile_id"]
            isOneToOne: false
            referencedRelation: "profiles"
            referencedColumns: ["id"]
          },
        ]
      }
      study_sessions: {
        Row: {
          completed_at: string | null
          id: string
          order: number
          scheduled_for: string
          skill_id: string
          study_plan_id: string
        }
        Insert: {
          completed_at?: string | null
          id?: string
          order?: number
          scheduled_for: string
          skill_id: string
          study_plan_id: string
        }
        Update: {
          completed_at?: string | null
          id?: string
          order?: number
          scheduled_for?: string
          skill_id?: string
          study_plan_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "study_sessions_skill_id_fkey"
            columns: ["skill_id"]
            isOneToOne: false
            referencedRelation: "skills"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "study_sessions_study_plan_id_fkey"
            columns: ["study_plan_id"]
            isOneToOne: false
            referencedRelation: "study_plans"
            referencedColumns: ["id"]
          },
        ]
      }
      subjects: {
        Row: {
          id: string
          name: string
          program_id: string
          slug: string
        }
        Insert: {
          id?: string
          name: string
          program_id: string
          slug: string
        }
        Update: {
          id?: string
          name?: string
          program_id?: string
          slug?: string
        }
        Relationships: [
          {
            foreignKeyName: "subjects_program_id_fkey"
            columns: ["program_id"]
            isOneToOne: false
            referencedRelation: "programs"
            referencedColumns: ["id"]
          },
        ]
      }
      topics: {
        Row: {
          class_id: string
          id: string
          order: number
          parent_id: string | null
          subject_id: string
          title: string
        }
        Insert: {
          class_id: string
          id?: string
          order?: number
          parent_id?: string | null
          subject_id: string
          title: string
        }
        Update: {
          class_id?: string
          id?: string
          order?: number
          parent_id?: string | null
          subject_id?: string
          title?: string
        }
        Relationships: [
          {
            foreignKeyName: "topics_class_id_fkey"
            columns: ["class_id"]
            isOneToOne: false
            referencedRelation: "classes"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "topics_parent_id_fkey"
            columns: ["parent_id"]
            isOneToOne: false
            referencedRelation: "topics"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "topics_subject_id_fkey"
            columns: ["subject_id"]
            isOneToOne: false
            referencedRelation: "subjects"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      is_staff: { Args: never; Returns: boolean }
    }
    Enums: {
      ai_message_role: "user" | "assistant" | "system"
      attemptable_type: "exercise"
      content_status:
        | "draft"
        | "under_review"
        | "validated"
        | "published"
        | "archived"
      difficulty_level: "easy" | "medium" | "hard"
      exam_rights_status:
        | "verified"
        | "permission_required"
        | "publicly_reusable"
        | "restricted"
        | "unknown"
      exercise_type:
        | "multiple_choice"
        | "true_false"
        | "short_answer"
        | "free_response"
      mock_exam_status: "in_progress" | "submitted"
      study_plan_status: "active" | "completed" | "cancelled"
      user_role: "student" | "parent" | "teacher" | "admin"
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  graphql_public: {
    Enums: {},
  },
  public: {
    Enums: {
      ai_message_role: ["user", "assistant", "system"],
      attemptable_type: ["exercise"],
      content_status: [
        "draft",
        "under_review",
        "validated",
        "published",
        "archived",
      ],
      difficulty_level: ["easy", "medium", "hard"],
      exam_rights_status: [
        "verified",
        "permission_required",
        "publicly_reusable",
        "restricted",
        "unknown",
      ],
      exercise_type: [
        "multiple_choice",
        "true_false",
        "short_answer",
        "free_response",
      ],
      mock_exam_status: ["in_progress", "submitted"],
      study_plan_status: ["active", "completed", "cancelled"],
      user_role: ["student", "parent", "teacher", "admin"],
    },
  },
} as const

