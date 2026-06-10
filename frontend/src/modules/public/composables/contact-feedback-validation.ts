import type {
    ContactFeedbackFormErrors,
    ContactFeedbackFormState,
} from "@/modules/public/types/contact.types";
import { normalizeContactFeedbackText } from "@/modules/public/composables/contact-feedback-form.state";

type Translator = (value: string) => string;

const MAX_FILES_COUNT = 5;
const MAX_FILE_SIZE = 5 * 1024 * 1024;
const ALLOWED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".pdf", ".doc", ".docx"];
const ALLOWED_FILE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
];

export function validateContactFeedbackFiles(
    files: File[],
    errors: ContactFeedbackFormErrors,
    tr: Translator,
): boolean {
    errors.attachments = "";

    if (!files.length) {
        return true;
    }

    if (files.length > MAX_FILES_COUNT) {
        errors.attachments = tr(`Можно прикрепить не более ${MAX_FILES_COUNT} файлов.`);
        return false;
    }

    const invalidExtensionFile = files.find((file) => {
        return !ALLOWED_FILE_EXTENSIONS.includes(getFileExtension(file.name));
    });

    if (invalidExtensionFile) {
        errors.attachments = tr(`Файл «${invalidExtensionFile.name}» имеет неподдерживаемый формат. Поддерживаются изображения, PDF, DOC и DOCX.`);
        return false;
    }

    const invalidTypeFile = files.find((file) => {
        return file.type && !ALLOWED_FILE_TYPES.includes(file.type);
    });

    if (invalidTypeFile) {
        errors.attachments = tr(`Файл «${invalidTypeFile.name}» имеет неподдерживаемый тип.`);
        return false;
    }

    const oversizedFile = files.find((file) => file.size > MAX_FILE_SIZE);

    if (oversizedFile) {
        errors.attachments = tr(`Файл «${oversizedFile.name}» больше 5 МБ.`);
        return false;
    }

    return true;
}

export function validateContactFeedbackForm(
    form: ContactFeedbackFormState,
    errors: ContactFeedbackFormErrors,
    tr: Translator,
): boolean {
    const fullName = normalizeContactFeedbackText(form.fullName);
    const email = normalizeContactFeedbackText(form.email);
    const message = form.message.trim();

    if (!fullName) {
        errors.fullName = tr("Укажите имя.");
    } else if (fullName.length < 2) {
        errors.fullName = tr("Имя должно содержать не менее 2 символов.");
    }

    if (!email) {
        errors.email = tr("Укажите email.");
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errors.email = tr("Введите корректный email.");
    }

    if (!message) {
        errors.message = tr("Введите сообщение.");
    } else if (message.length < 10) {
        errors.message = tr("Сообщение должно содержать не менее 10 символов.");
    } else if (message.length > 5000) {
        errors.message = tr("Сообщение не должно превышать 5000 символов.");
    }

    if (!form.isPersonalDataConsent) {
        errors.isPersonalDataConsent = tr("Необходимо согласие на обработку персональных данных.");
    }

    validateContactFeedbackFiles(form.attachments, errors, tr);

    return !Object.values(errors).some(Boolean);
}

function getFileExtension(fileName: string): string {
    const dotIndex = fileName.lastIndexOf(".");

    return dotIndex === -1 ? "" : fileName.slice(dotIndex).toLowerCase();
}
