import type {
    JoinRequestStatusApi,
    JoinRequestTypeApi,
    StatusTone,
    StudyFormApi,
    StudyGroupStatusApi,
    TeacherEmploymentTypeApi,
} from "../types";

export interface SelectOption<TValue extends string = string> {
    label: string;
    value: TValue;
}

export interface StatusOption<TValue extends string = string>
    extends SelectOption<TValue> {
    tone: StatusTone;
    className: string;
}

export const BOOLEAN_FILTER_OPTIONS: SelectOption<"true" | "false">[] = [
    {
        label: "Да",
        value: "true",
    },
    {
        label: "Нет",
        value: "false",
    },
];

export const STUDY_GROUP_STATUS_OPTIONS: StatusOption<StudyGroupStatusApi>[] = [
    {
        label: "Активна",
        value: "active",
        tone: "success",
        className: "org-table__status--active",
    },
    {
        label: "Архив",
        value: "archived",
        tone: "muted",
        className: "org-table__status--archived",
    },
    {
        label: "Выпущена",
        value: "graduated",
        tone: "neutral",
        className: "org-table__status--inactive",
    },
    {
        label: "Черновик",
        value: "draft",
        tone: "warning",
        className: "org-table__status--pending",
    },
];

export const STUDY_FORM_OPTIONS: SelectOption<StudyFormApi>[] = [
    {
        label: "Очная",
        value: "full_time",
    },
    {
        label: "Очно-заочная",
        value: "part_time",
    },
    {
        label: "Дистанционная",
        value: "distance",
    },
    {
        label: "Смешанная",
        value: "mixed",
    },
];

export const TEACHER_EMPLOYMENT_TYPE_OPTIONS: SelectOption<TeacherEmploymentTypeApi>[] = [
    {
        label: "Основное место работы",
        value: "full_time",
    },
    {
        label: "Совместительство",
        value: "part_time",
    },
    {
        label: "Договор",
        value: "contract",
    },
    {
        label: "Внешний преподаватель",
        value: "external",
    },
];

export const JOIN_REQUEST_TYPE_OPTIONS: SelectOption<JoinRequestTypeApi>[] = [
    {
        label: "Преподаватель в организацию",
        value: "teacher_to_organization",
    },
    {
        label: "Учащийся в группу",
        value: "learner_to_group",
    },
    {
        label: "Родитель к учащемуся",
        value: "guardian_to_learner",
    },
];

export const JOIN_REQUEST_STATUS_OPTIONS: StatusOption<JoinRequestStatusApi>[] = [
    {
        label: "Ожидает",
        value: "pending",
        tone: "warning",
        className: "org-table__status--pending",
    },
    {
        label: "Принята",
        value: "approved",
        tone: "success",
        className: "org-table__status--approved",
    },
    {
        label: "Отклонена",
        value: "rejected",
        tone: "danger",
        className: "org-table__status--rejected",
    },
    {
        label: "Отменена",
        value: "cancelled",
        tone: "muted",
        className: "org-table__status--inactive",
    },
    {
        label: "Истекла",
        value: "expired",
        tone: "muted",
        className: "org-table__status--inactive",
    },
];

export const ACTIVE_STATUS_OPTION: StatusOption<"active"> = {
    label: "Активно",
    value: "active",
    tone: "success",
    className: "org-table__status--active",
};

export const INACTIVE_STATUS_OPTION: StatusOption<"inactive"> = {
    label: "Неактивно",
    value: "inactive",
    tone: "muted",
    className: "org-table__status--inactive",
};

export const PRIMARY_STATUS_OPTION: StatusOption<"primary"> = {
    label: "Основная",
    value: "primary",
    tone: "accent",
    className: "org-table__status--verified",
};

export const SECONDARY_STATUS_OPTION: StatusOption<"secondary"> = {
    label: "Дополнительная",
    value: "secondary",
    tone: "neutral",
    className: "org-table__status--inactive",
};