import type {
    CurrentProfileDto,
    ProfileRoleCode,
    ProfileRoleSectionModel,
} from "@/modules/profile/types/profile.types";

export function mapCurrentProfileToRoleSection(
    dto: CurrentProfileDto,
): ProfileRoleSectionModel {
    const roleCode = dto.active_role.code;
    const roleProfile = dto.role_profile;

    if (isTeacherRole(roleCode)) {
        return {
            roleCode,
            title: "Профессиональный профиль преподавателя",
            text: "В этом разделе собрана информация, связанная с преподавательской ролью: специализация, нагрузка, дисциплины и методическая зона ответственности.",
            facts: [
                { label: "Основная роль", value: dto.active_role.label },
                { label: "Организация", value: getString(roleProfile.organization) },
                { label: "Подразделение", value: getString(roleProfile.department) },
                { label: "Должность", value: getString(roleProfile.position) },
                { label: "Публичный заголовок", value: getString(roleProfile.public_title) },
                { label: "Педагогический стаж", value: formatExperience(roleProfile.experience_years) },
                { label: "Статус", value: getString(roleProfile.status) },
            ],
            tags: splitTags(getString(roleProfile.public_title)),
            groups: [],
            education: [
                { title: "Образование", text: getString(roleProfile.education) },
                { title: "Профессиональные достижения", text: getString(roleProfile.achievements) },
            ],
        };
    }

    if (roleCode === "learner") {
        return {
            roleCode,
            title: "Профиль студента",
            text: "Здесь собрана учебная информация студента: организация, группа, направление и текущий статус обучения.",
            facts: [
                { label: "Основная роль", value: dto.active_role.label },
                { label: "Организация", value: getString(roleProfile.organization) },
                { label: "Отделение", value: getString(roleProfile.department) },
                { label: "Группа", value: getString(roleProfile.group) },
                { label: "Куратор", value: getString(roleProfile.curator) },
                { label: "Год поступления", value: getString(roleProfile.admission_year) },
                { label: "Статус", value: getString(roleProfile.status) },
            ],
            tags: [],
            groups: [],
            education: [],
        };
    }

    return {
        roleCode,
        title: "Роль пользователя",
        text: "Здесь отображается информация, связанная с активной ролью пользователя внутри платформы.",
        facts: [{ label: "Активная роль", value: dto.active_role.label }],
        tags: [],
        groups: [],
        education: [],
    };
}

function isTeacherRole(roleCode: ProfileRoleCode): boolean {
    return ["teacher", "curator", "methodist", "organizer", "mentor"].includes(roleCode);
}

function getString(value: unknown): string {
    if (typeof value === "string" && value.trim()) {
        return value;
    }

    return typeof value === "number" ? String(value) : "Не указано";
}

function splitTags(value: string): string[] {
    return !value || value === "Не указано"
        ? []
        : value.split(/[·,;/]/).map((item) => item.trim()).filter(Boolean);
}

function formatExperience(value: unknown): string {
    return typeof value === "number" ? `${value} лет` : getString(value);
}
