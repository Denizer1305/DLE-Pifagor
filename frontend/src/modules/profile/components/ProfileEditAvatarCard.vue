<script setup lang="ts">
import { ref } from "vue";

import ProfileAvatarCropModal from "@/modules/profile/components/ProfileAvatarCropModal.vue";

interface Props {
    avatarUrl: string;
    avatarAlt: string;
    isSubmitting?: boolean;
}

interface Emits {
    (event: "upload", file: File): void;
    (event: "delete"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
const fileForCropping = ref<File | null>(null);

function handleFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (file) {
        fileForCropping.value = file;
    }

    input.value = "";
}

function confirmCrop(file: File): void {
    fileForCropping.value = null;
    emit("upload", file);
}
</script>

<template>
    <section class="profile-edit-section profile-edit-section-avatar fade-in visible">
        <div class="profile-edit-section-head">
            <div>
                <div class="profile-edit-section-topline">
                    <i class="fas fa-image"></i>
                    Фото профиля
                </div>

                <h2 class="profile-edit-section-title">
                    Аватар пользователя
                </h2>

                <p class="profile-edit-section-text">
                    Загрузите или замените изображение, которое будет отображаться в кабинете и профиле.
                </p>
            </div>
        </div>

        <div class="profile-edit-card profile-edit-avatar-card">
            <div class="profile-edit-avatar-preview">
                <img
                    :src="avatarUrl"
                    :alt="avatarAlt"
                />
            </div>

            <div class="profile-edit-avatar-content">
                <div class="profile-edit-avatar-actions">
                    <label class="profile-edit-upload-btn">
                        <input
                            type="file"
                            accept="image/png,image/jpeg,image/webp"
                            hidden
                            :disabled="isSubmitting"
                            @change="handleFileChange"
                        />

                        <i class="fas fa-upload"></i>
                        Загрузить фото
                    </label>

                    <button
                        type="button"
                        class="profile-edit-remove-btn"
                        :disabled="isSubmitting"
                        @click="emit('delete')"
                    >
                        <i class="fas fa-trash"></i>
                        Удалить фото
                    </button>
                </div>

                <p class="profile-edit-helper">
                    Поддерживаются изображения JPG, PNG, WEBP. Рекомендуемый формат — квадратное фото.
                </p>
            </div>
        </div>
    </section>

    <ProfileAvatarCropModal
        v-if="fileForCropping"
        :file="fileForCropping"
        :is-submitting="isSubmitting"
        @cancel="fileForCropping = null"
        @confirm="confirmCrop"
    />
</template>
