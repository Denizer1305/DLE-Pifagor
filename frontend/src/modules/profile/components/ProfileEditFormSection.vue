<script setup lang="ts">
import BaseSelect from "@/components/base/BaseSelect.vue";
import ProfileCitySelect from "@/modules/profile/components/ProfileCitySelect.vue";
import { formatRussianPhone } from "@/modules/auth/composables/usePhoneMask";
import type {
    ProfileEditFormErrors,
    ProfileCitySuggestion,
    ProfileEditFormState,
} from "@/modules/profile/types/profile-edit.types";

interface Props {
    form: ProfileEditFormState;
    errors: ProfileEditFormErrors;
    citySuggestions: ProfileCitySuggestion[];
    isCitySuggestionsLoading?: boolean;
}

interface Emits {
    (event: "search-city", value: string): void;
    (event: "select-city", suggestion: ProfileCitySuggestion): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();
const genderOptions = [
    { value: "female", label: "Женский" },
    { value: "male", label: "Мужской" },
    { value: "not_specified", label: "Не указывать" },
];
const contactMethodOptions = [
    { value: "email", label: "Электронная почта" },
    { value: "phone", label: "Телефон" },
    { value: "vk", label: "VK" },
    { value: "max", label: "MAX" },
];

function handlePhoneInput(event: Event): void {
    const input = event.target as HTMLInputElement;

    props.form.phone = formatRussianPhone(input.value);
}
</script>

<template>
    <section class="profile-edit-section fade-in visible">
        <div class="profile-edit-section-head">
            <div>
                <div class="profile-edit-section-topline">
                    <i class="fas fa-id-card"></i>
                    Общие данные
                </div>

                <h2 class="profile-edit-section-title">
                    Личная информация
                </h2>

                <p class="profile-edit-section-text">
                    Основные сведения о пользователе, которые используются в профиле и системе.
                </p>
            </div>
        </div>

        <div class="profile-edit-card">
            <div class="profile-edit-grid profile-edit-grid-3">
                <div class="profile-edit-field">
                    <label for="profile-last-name">Фамилия</label>
                    <input
                        id="profile-last-name"
                        v-model="form.lastName"
                        type="text"
                    />
                    <span
                        v-if="errors.lastName"
                        class="profile-edit-field-status"
                    >
                        {{ errors.lastName }}
                    </span>
                </div>

                <div class="profile-edit-field">
                    <label for="profile-first-name">Имя</label>
                    <input
                        id="profile-first-name"
                        v-model="form.firstName"
                        type="text"
                    />
                    <span
                        v-if="errors.firstName"
                        class="profile-edit-field-status"
                    >
                        {{ errors.firstName }}
                    </span>
                </div>

                <div class="profile-edit-field">
                    <label for="profile-middle-name">Отчество</label>
                    <input
                        id="profile-middle-name"
                        v-model="form.middleName"
                        type="text"
                    />
                </div>

                <div class="profile-edit-field">
                    <label for="profile-birth-date">Дата рождения</label>
                    <input
                        id="profile-birth-date"
                        v-model="form.birthDate"
                        type="date"
                    />
                </div>

                <div class="profile-edit-field">
                    <label for="profile-gender">Пол</label>
                    <BaseSelect
                        id="profile-gender"
                        v-model="form.gender"
                        :options="genderOptions"
                        aria-label="Выбрать пол"
                    />
                </div>

                <div class="profile-edit-field">
                    <label for="profile-city">Город</label>
                    <ProfileCitySelect
                        v-model="form.city"
                        :suggestions="citySuggestions"
                        :is-loading="isCitySuggestionsLoading"
                        @search="emit('search-city', $event)"
                        @select="emit('select-city', $event)"
                    />
                </div>

                <div class="profile-edit-field profile-edit-field-full">
                    <label for="profile-about">О себе</label>
                    <textarea
                        id="profile-about"
                        v-model="form.about"
                        placeholder="Краткая информация о пользователе..."
                    ></textarea>
                </div>
            </div>
        </div>
    </section>

    <section class="profile-edit-section profile-edit-section-contacts fade-in visible">
        <div class="profile-edit-section-head">
            <div>
                <div class="profile-edit-section-topline">
                    <i class="fas fa-paper-plane"></i>
                    Связь и аккаунт
                </div>

                <h2 class="profile-edit-section-title">
                    Контакты и способы связи
                </h2>

                <p class="profile-edit-section-text">
                    Данные, по которым с пользователем можно связаться внутри и вне платформы.
                </p>
            </div>
        </div>

        <div class="profile-edit-card">
            <div class="profile-edit-grid profile-edit-grid-2">
                <div class="profile-edit-field">
                    <label for="profile-email">Электронная почта</label>
                    <input
                        id="profile-email"
                        v-model="form.email"
                        type="email"
                        disabled
                    />
                    <span class="profile-edit-field-status is-success">
                        <i class="fas fa-check-circle"></i>
                        Email меняется отдельным подтверждением
                    </span>
                </div>

                <div class="profile-edit-field">
                    <label for="profile-phone">Телефон</label>
                    <input
                        id="profile-phone"
                        v-model="form.phone"
                        type="tel"
                        inputmode="tel"
                        placeholder="+7 999 123-45-67"
                        @input="handlePhoneInput"
                    />
                    <span
                        v-if="errors.phone"
                        class="profile-edit-field-status"
                    >
                        {{ errors.phone }}
                    </span>
                </div>

                <div class="profile-edit-field">
                    <label for="profile-backup-email">Резервный email</label>
                    <input
                        id="profile-backup-email"
                        v-model="form.backupEmail"
                        type="email"
                        placeholder="backup@example.ru"
                    />
                    <span
                        v-if="errors.backupEmail"
                        class="profile-edit-field-status"
                    >
                        {{ errors.backupEmail }}
                    </span>
                </div>

                <div class="profile-edit-field">
                    <label for="profile-vk">VK</label>
                    <input
                        id="profile-vk"
                        v-model="form.vkUrl"
                        type="url"
                    />
                </div>

                <div class="profile-edit-field">
                    <label for="profile-max">MAX</label>
                    <input
                        id="profile-max"
                        v-model="form.maxUrl"
                        type="text"
                    />
                </div>

                <div class="profile-edit-field">
                    <label for="profile-contact-method">Предпочтительный способ связи</label>
                    <BaseSelect
                        id="profile-contact-method"
                        v-model="form.preferredContactMethod"
                        :options="contactMethodOptions"
                        aria-label="Выбрать способ связи"
                    />
                </div>
            </div>
        </div>
    </section>

    <section class="profile-edit-section fade-in visible">
        <div class="profile-edit-section-head">
            <div>
                <div class="profile-edit-section-topline">
                    <i class="fas fa-eye"></i>
                    Отображение и уведомления
                </div>

                <h2 class="profile-edit-section-title">
                    Параметры отображения профиля
                </h2>

                <p class="profile-edit-section-text">
                    Настройки того, как профиль показывается в системе и какие уведомления получает пользователь.
                </p>
            </div>
        </div>

        <div class="profile-edit-card">
            <div class="profile-edit-toggle-list">
                <label class="profile-edit-toggle">
                    <input
                        v-model="form.showEmail"
                        type="checkbox"
                    />
                    <span class="profile-edit-toggle-ui"></span>
                    <span class="profile-edit-toggle-copy">
                        <strong>Показывать email в профиле</strong>
                        <span>Электронная почта будет доступна в публичной карточке профиля.</span>
                    </span>
                </label>

                <label class="profile-edit-toggle">
                    <input
                        v-model="form.showPhone"
                        type="checkbox"
                    />
                    <span class="profile-edit-toggle-ui"></span>
                    <span class="profile-edit-toggle-copy">
                        <strong>Показывать телефон</strong>
                        <span>Телефон будет отображаться в карточке профиля и контактах.</span>
                    </span>
                </label>

                <label class="profile-edit-toggle">
                    <input
                        v-model="form.emailNotifications"
                        type="checkbox"
                    />
                    <span class="profile-edit-toggle-ui"></span>
                    <span class="profile-edit-toggle-copy">
                        <strong>Email-уведомления</strong>
                        <span>Получение системных и учебных уведомлений на почту.</span>
                    </span>
                </label>

                <label class="profile-edit-toggle">
                    <input
                        v-model="form.pushNotifications"
                        type="checkbox"
                    />
                    <span class="profile-edit-toggle-ui"></span>
                    <span class="profile-edit-toggle-copy">
                        <strong>Внутрисистемные уведомления</strong>
                        <span>Показывать уведомления о событиях внутри платформы.</span>
                    </span>
                </label>
            </div>
        </div>
    </section>
</template>
