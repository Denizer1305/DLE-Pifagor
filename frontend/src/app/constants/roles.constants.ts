export const ROLE_CODES = {
    SUPERADMIN: "superadmin",
    PLATFORM_ADMIN: "platform_admin",
    ADMIN: "admin",
    DIRECTOR: "director",
    ORG_ADMIN: "org_admin",
    DEPARTMENT_HEAD: "department_head",
    CURATOR: "curator",
    TEACHER: "teacher",
    STUDENT: "student",
    LEARNER: "learner",
    GUARDIAN: "guardian",
    METHODIST: "methodist",
    ORGANIZER: "organizer",
    MENTOR: "mentor",
} as const;

export type RoleCode = typeof ROLE_CODES[keyof typeof ROLE_CODES];

export const ROLE_LABELS: Record<RoleCode, string> = {
    [ROLE_CODES.SUPERADMIN]: "Суперадминистратор",
    [ROLE_CODES.PLATFORM_ADMIN]: "Администратор платформы",
    [ROLE_CODES.ADMIN]: "Администратор",
    [ROLE_CODES.DIRECTOR]: "Директор",
    [ROLE_CODES.ORG_ADMIN]: "Администратор организации",
    [ROLE_CODES.DEPARTMENT_HEAD]: "Заведующий отделением",
    [ROLE_CODES.CURATOR]: "Куратор",
    [ROLE_CODES.TEACHER]: "Преподаватель",
    [ROLE_CODES.STUDENT]: "Студент",
    [ROLE_CODES.LEARNER]: "Учащийся",
    [ROLE_CODES.GUARDIAN]: "Родитель",
    [ROLE_CODES.METHODIST]: "Методист",
    [ROLE_CODES.ORGANIZER]: "Педагог-организатор",
    [ROLE_CODES.MENTOR]: "Педагог-наставник",
};
