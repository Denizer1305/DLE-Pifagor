import { onBeforeUnmount, onMounted, type Ref } from "vue";

interface FloatingCanvasOptions {
    pointsCount?: number;
    mobilePointsCount?: number;
    lineDistance?: number;
    wavesEnabled?: boolean;
    particlesEnabled?: boolean;
    resizeTargetSelector?: string;
}

interface FloatingCanvasConfig {
    pointsCount: number;
    mobilePointsCount: number;
    lineDistance: number;
    wavesEnabled: boolean;
    particlesEnabled: boolean;
    resizeTargetSelector: string;
}

interface ThemeColors {
    particle: string;
    line: string;
    wave: string;
}

function getThemeColors(): ThemeColors {
    const isDark = document.body.classList.contains("dark-theme");

    return {
        particle: isDark ? "rgba(255,255,255,0.12)" : "rgba(74,111,165,0.08)",
        line: isDark ? "rgba(255,255,255," : "rgba(74,111,165,",
        wave: isDark ? "rgba(255,255,255," : "rgba(74,111,165,",
    };
}

class FloatingParticle {
    public x: number;
    public y: number;
    public size: number;
    public speedX: number;
    public speedY: number;

    public constructor(width: number, height: number) {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.size = Math.random() * 2 + 0.8;
        this.speedX = Math.random() * 0.35 - 0.175;
        this.speedY = Math.random() * 0.35 - 0.175;
    }

    public update(width: number, height: number): void {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x > width) {
            this.x = 0;
        }

        if (this.x < 0) {
            this.x = width;
        }

        if (this.y > height) {
            this.y = 0;
        }

        if (this.y < 0) {
            this.y = height;
        }
    }

    public draw(ctx: CanvasRenderingContext2D): void {
        const colors = getThemeColors();

        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = colors.particle;
        ctx.fill();
    }
}

class FloatingWave {
    public y: number;
    public amplitude: number;
    public speed: number;
    public opacity: number;
    public offset: number;

    public constructor(y: number, amplitude: number, speed: number, opacity: number) {
        this.y = y;
        this.amplitude = amplitude;
        this.speed = speed;
        this.opacity = opacity;
        this.offset = Math.random() * Math.PI * 2;
    }

    public update(): void {
        this.offset += this.speed;
    }

    public draw(ctx: CanvasRenderingContext2D, width: number, index: number): void {
        const colors = getThemeColors();

        ctx.beginPath();

        for (let x = 0; x <= width; x += 12) {
            const waveY =
                this.y +
                Math.sin(x * 0.008 + this.offset) * this.amplitude +
                Math.cos(x * 0.004 + this.offset * 0.7) * (this.amplitude * 0.35);

            if (x === 0) {
                ctx.moveTo(x, waveY);
            } else {
                ctx.lineTo(x, waveY);
            }
        }

        ctx.strokeStyle = `${colors.wave}${this.opacity})`;
        ctx.lineWidth = index % 2 === 0 ? 1 : 0.75;
        ctx.stroke();
    }
}

export function useFloatingCanvas(
    canvasRef: Ref<HTMLCanvasElement | null>,
    options: FloatingCanvasOptions = {},
) {
    const config: FloatingCanvasConfig = {
        pointsCount: options.pointsCount ?? 42,
        mobilePointsCount: options.mobilePointsCount ?? 24,
        lineDistance: options.lineDistance ?? 90,
        wavesEnabled: options.wavesEnabled ?? true,
        particlesEnabled: options.particlesEnabled ?? true,
        resizeTargetSelector: options.resizeTargetSelector ?? "",
    };

    let canvas: HTMLCanvasElement | null = null;
    let ctx: CanvasRenderingContext2D | null = null;
    let animationFrame: number | null = null;
    let width = 0;
    let height = 0;
    let particles: FloatingParticle[] = [];
    let waves: FloatingWave[] = [];

    const prefersReducedMotion =
        typeof window !== "undefined" &&
        Boolean(window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches);

    function getCanvasHeight(): number {
        if (config.resizeTargetSelector) {
            const target = document.querySelector<HTMLElement>(config.resizeTargetSelector);

            if (target) {
                return target.offsetHeight;
            }
        }

        const parent = canvas?.parentElement;

        if (parent) {
            return parent.offsetHeight;
        }

        return window.innerHeight;
    }

    function createParticles(): void {
        particles = [];

        const count = window.innerWidth < 768
            ? config.mobilePointsCount
            : config.pointsCount;

        for (let index = 0; index < count; index += 1) {
            particles.push(new FloatingParticle(width, height));
        }
    }

    function createWaves(): void {
        waves = [
            new FloatingWave(height * 0.18, 8, 0.012, 0.1),
            new FloatingWave(height * 0.34, 12, 0.01, 0.08),
            new FloatingWave(height * 0.52, 10, 0.014, 0.07),
            new FloatingWave(height * 0.72, 14, 0.009, 0.07),
            new FloatingWave(height * 0.86, 7, 0.013, 0.08),
        ];
    }

    function resizeCanvas(): void {
        if (!canvas) {
            return;
        }

        const pixelRatio = window.devicePixelRatio || 1;

        width = window.innerWidth;
        height = getCanvasHeight();

        canvas.width = Math.floor(width * pixelRatio);
        canvas.height = Math.floor(height * pixelRatio);
        canvas.style.width = `${width}px`;
        canvas.style.height = `${height}px`;

        const canvasContext = canvas.getContext("2d");

        if (!canvasContext) {
            ctx = null;
            return;
        }

        ctx = canvasContext;
        ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);

        createParticles();
        createWaves();
    }

    function drawParticleLines(activeContext: CanvasRenderingContext2D): void {
        const colors = getThemeColors();

        for (let firstIndex = 0; firstIndex < particles.length; firstIndex += 1) {
            const firstParticle = particles[firstIndex];

            if (!firstParticle) {
                continue;
            }

            for (let secondIndex = firstIndex + 1; secondIndex < particles.length; secondIndex += 1) {
                const secondParticle = particles[secondIndex];

                if (!secondParticle) {
                    continue;
                }

                const dx = firstParticle.x - secondParticle.x;
                const dy = firstParticle.y - secondParticle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < config.lineDistance) {
                    const opacity = 0.05 * (1 - distance / config.lineDistance);

                    activeContext.beginPath();
                    activeContext.strokeStyle = `${colors.line}${opacity})`;
                    activeContext.lineWidth = 0.5;
                    activeContext.moveTo(firstParticle.x, firstParticle.y);
                    activeContext.lineTo(secondParticle.x, secondParticle.y);
                    activeContext.stroke();
                }
            }
        }
    }

    function animate(): void {
        if (!ctx) {
            return;
        }

        const activeContext = ctx;

        activeContext.clearRect(0, 0, width, height);

        if (config.wavesEnabled) {
            waves.forEach((wave, index) => {
                wave.update();
                wave.draw(activeContext, width, index);
            });
        }

        if (config.particlesEnabled) {
            particles.forEach((particle) => {
                particle.update(width, height);
                particle.draw(activeContext);
            });

            drawParticleLines(activeContext);
        }

        animationFrame = window.requestAnimationFrame(animate);
    }

    function startCanvas(): void {
        canvas = canvasRef.value;

        if (!canvas || prefersReducedMotion) {
            return;
        }

        resizeCanvas();

        if (!ctx) {
            return;
        }

        animate();

        window.addEventListener("resize", resizeCanvas, {
            passive: true,
        });
    }

    function stopCanvas(): void {
        if (animationFrame !== null) {
            window.cancelAnimationFrame(animationFrame);
        }

        window.removeEventListener("resize", resizeCanvas);

        animationFrame = null;
        canvas = null;
        ctx = null;
        particles = [];
        waves = [];
    }

    onMounted(() => {
        startCanvas();
    });

    onBeforeUnmount(() => {
        stopCanvas();
    });

    return {
        startCanvas,
        stopCanvas,
        resizeCanvas,
    };
}
