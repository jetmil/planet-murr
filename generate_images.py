# -*- coding: utf-8 -*-
"""
Генератор иллюстраций для книги "ПЛАНЕТА МУРР"
Космоопера о котах, драконах и птицах
Использует ComfyUI API с Qwen-Image моделью
"""

import requests
import json
import time
import os
import random
from pathlib import Path

# Обход прокси для локальных подключений
os.environ['NO_PROXY'] = '127.0.0.1,localhost'
os.environ['no_proxy'] = '127.0.0.1,localhost'
if 'http_proxy' in os.environ:
    del os.environ['http_proxy']
if 'https_proxy' in os.environ:
    del os.environ['https_proxy']

# Конфигурация
COMFYUI_URL = "http://127.0.0.1:8190"

import platform
if platform.system() == "Linux":
    OUTPUT_DIR = Path("/mnt/c/Users/PC/planet-murr/images")
else:
    OUTPUT_DIR = Path(r"C:\Users\PC\planet-murr\images")
OUTPUT_DIR.mkdir(exist_ok=True)

# === ПЕРСОНАЖИ ===
CHARACTER_PROMPTS = {
    "char_murka": {
        "title": "Мурка - главная героиня",
        "prompt": "portrait of a grey tabby cat with heterochromia eyes one green one yellow, tired cynical expression, wearing simple office clothes, bureaucrat aesthetic, sitting at desk with papers, muted grey tones, photorealistic cat, detailed fur texture, melancholic atmosphere, 8k",
        "negative": "text, letters, anime, cartoon, dog, human, low quality, blurry"
    },
    "char_ryzhik": {
        "title": "Рыжик - световой кот проводник",
        "prompt": "portrait of glowing orange ginger cat with ethereal bioluminescent fur, mystical aura, slightly crazy wise eyes, ragged appearance like a homeless wanderer, golden light emanating from fur, mysterious prophet aesthetic, photorealistic cat, cosmic background, 8k",
        "negative": "text, letters, anime, cartoon, dog, human, low quality"
    },
    "char_zolotoy": {
        "title": "Золотой - дракон на солнце",
        "prompt": "majestic white dragon with golden eyes living inside the sun, scales made of pure light, wings of solar flares, gentle loving expression, cosmic scale creature, plasma and fire swirling around, young dragon 127000 years old, romantic ancient being, photorealistic fantasy, 8k",
        "negative": "text, letters, anime, cartoon, scary, evil, low quality"
    },
    "char_baton": {
        "title": "Батон - криминальный авторитет",
        "prompt": "portrait of old scarred one-eyed cat crime boss, ragged patchy fur, missing ear chunks, sitting in ruined throne chair, philosophical dangerous expression, holding bottle, dim lighting underground lair, mafia don aesthetic, photorealistic cat, gritty atmosphere, 8k",
        "negative": "text, letters, anime, cartoon, dog, cute, low quality"
    },
    "char_golysh": {
        "title": "Отец Голыш - верховный жрец сфинксов",
        "prompt": "portrait of ancient hairless sphynx cat priest, completely bald wrinkled skin, blind milky white eyes that see truth, wearing simple grey robes, wise mysterious smile, holding cucumber ceremonially, temple background with candles, photorealistic sphynx cat, mystical atmosphere, 8k",
        "negative": "text, letters, anime, cartoon, fur, hairy, low quality"
    },
    "char_birds": {
        "title": "Птицы - Империя Клюва",
        "prompt": "menacing alien birds in mechanical exoskeletons, featherless skeletal avians, cold empty eyes, biomechanical armor suits, fleet of ships behind them, dark space background, technological horror aesthetic, empire of destruction, photorealistic sci-fi, 8k",
        "negative": "text, letters, anime, cartoon, cute, friendly, low quality"
    }
}

# === ГЛАВЫ ===
CHAPTER_PROMPTS = {
    "ch00_prologue": {
        "title": "Пролог - Мир каким его знают",
        "prompt": "tidally locked planet with eternal day on one side and eternal night on other, middle zone twilight city of cats, giant sun on horizon as wall of fire, cosmic view from space, unique planetary system, photorealistic sci-fi worldbuilding, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "ch01_another_day": {
        "title": "Глава 1 - Ещё один день",
        "prompt": "grey cat bureaucrat at desk in dystopian ministry office, stamping documents with REJECTED, queue of nervous cats waiting, Soviet aesthetic mixed with cats, depressing fluorescent lighting, beauty rating system posters, photorealistic, 8k",
        "negative": "text, letters, readable words, anime, cartoon, low quality"
    },
    "ch02_voice": {
        "title": "Глава 2 - Тот кто слышит",
        "prompt": "glowing orange cat wandering through neon city streets at night, hearing mysterious voice from the sky, looking up at giant sun on horizon, urban twilight zone, bioluminescent fur in darkness, mystical calling, photorealistic, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "ch03_meeting": {
        "title": "Глава 3 - Тот кто ищет",
        "prompt": "two cats meeting in government office, grey tabby and glowing orange cat, tense dramatic moment, one being arrested by guards, reaching toward each other, bureaucratic nightmare, dramatic lighting, photorealistic, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "ch04_dream": {
        "title": "Глава 4 - Сон",
        "prompt": "grey cat sleeping having vivid dream of flying through golden light, dream bubble showing dragon and stars, first time without sleeping pills, tears on pillow, bedroom with moonlight, ethereal dream sequence, photorealistic, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "ch05_sphynx": {
        "title": "Глава 5 - Лысые",
        "prompt": "ancient stone temple of hairless sphynx cats in cold mountains, mysterious cult aesthetic, cucumbers arranged in ritual circles, orange cat entering through massive door, mist and incense, sacred geometry, photorealistic fantasy architecture, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "ch06_revelation": {
        "title": "Глава 6 - Откровение",
        "prompt": "old blind sphynx priest revealing cosmic truth to grey cat, ancient murals showing dragons living in sun, prophecy scene with candlelight, dramatic revelation moment, temple interior with pillars, photorealistic, 8k",
        "negative": "text, letters, readable writing, anime, cartoon, low quality"
    },
    "ch07_ritual": {
        "title": "Глава 7 - Голос из огня",
        "prompt": "mystical ritual scene with cats in circle of glowing cucumbers, orange cat as antenna glowing bright, grey cat in trance receiving vision of dragon, golden light filling temple, spiritual connection moment, photorealistic fantasy, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "ch08_baton": {
        "title": "Глава 8 - Батон",
        "prompt": "crime boss cat meeting in abandoned mine, one-eyed old cat on ruined throne, three heroes standing before him, tense negotiation scene, dim lighting dramatic shadows, criminal underworld aesthetic, photorealistic, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "ch09_stars_fade": {
        "title": "Глава 9 - Звёзды гаснут",
        "prompt": "night sky over cat city with stars visibly disappearing, cats on rooftops pointing at empty patches in sky, panic beginning, astronomers with telescopes, cosmic horror approaching, beautiful but terrifying, photorealistic, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "ch10_broadcast": {
        "title": "Глава 10 - Трансляция",
        "prompt": "cats storming TV station control room, screens showing dragon appearing to entire world, millions of cats watching in streets, golden light from all screens, revolution moment, media takeover scene, photorealistic, 8k",
        "negative": "text, letters, readable text on screens, anime, cartoon, low quality"
    },
    "ch11_battle": {
        "title": "Глава 11 - Битва за солнце",
        "prompt": "epic space battle, white dragons emerging from sun attacking alien bird fleet, ships exploding in solar flares, Dyson sphere being destroyed, cosmic scale warfare, golden light versus dark metal, photorealistic sci-fi epic, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "ch12_after": {
        "title": "Глава 12 - После",
        "prompt": "cat city celebrating victory, fireworks over skyline, cats hugging in streets, sun shining brighter than ever, new hope atmosphere, triumphant aftermath scene, warm golden light, photorealistic, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "ch13_epilogue": {
        "title": "Эпилог - Рассвет",
        "prompt": "grey cat and orange cat standing at edge of fire zone looking at sun, peaceful contemplation, new world beginning, dragon visible as golden silhouette in sun, sunrise over cat planet, bittersweet hopeful ending, photorealistic, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    }
}

# === КЛЮЧЕВЫЕ СОБЫТИЯ ===
EVENT_PROMPTS = {
    "event_ministry": {
        "title": "Министерство Эстетики",
        "prompt": "massive brutalist government building with cat beauty rating system, long queues of cats waiting for evaluation, dystopian architecture, propaganda posters showing ideal cats, oppressive atmosphere, social credit aesthetic, photorealistic, 8k",
        "negative": "text, letters, readable signs, anime, cartoon, low quality"
    },
    "event_peklo": {
        "title": "Пекло - раскалённая зона",
        "prompt": "hellish landscape near the sun side of tidally locked planet, cracked burning ground, heat waves distorting air, exile zone for low-rated cats, desperate figures in distance, fire wall on horizon, photorealistic harsh environment, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "event_merzlota": {
        "title": "Мерзлота - ледяная тьма",
        "prompt": "frozen dark side of tidally locked planet, eternal night with bioluminescent cats, ice structures, aurora in black sky, cold blue atmosphere, survival settlement, photorealistic frozen wasteland, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "event_dragon_vision": {
        "title": "Видение дракона",
        "prompt": "first person view of dragon vision, swimming through pure golden light, feeling of ancient love, memories of dancing between stars, ethereal romantic cosmic scene, warmth and belonging, photorealistic fantasy, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "event_bird_fleet": {
        "title": "Флот Империи Клюва",
        "prompt": "massive alien bird armada approaching star system, thousands of dark metallic ships, partially constructed Dyson sphere around sun, ominous invasion fleet, cosmic horror scale, photorealistic sci-fi, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "event_collective_belief": {
        "title": "Коллективная вера",
        "prompt": "millions of cats across planet simultaneously believing, golden energy rising from cities, connecting to sun, prayer-like scene but with cats, power of faith visualization, light beams converging, photorealistic spiritual moment, 8k",
        "negative": "text, letters, anime, cartoon, low quality"
    },
    "cover": {
        "title": "Обложка книги",
        "prompt": "book cover composition, grey cat with heterochromia looking up at giant sun where white dragon is visible, cosmic scale, tidally locked planet below, epic fantasy sci-fi mashup, dramatic lighting, title space at top, photorealistic, 8k",
        "negative": "text, letters, title, words, anime, cartoon, low quality"
    }
}

# Объединяем все промпты
ALL_PROMPTS = {}
ALL_PROMPTS.update(CHARACTER_PROMPTS)
ALL_PROMPTS.update(CHAPTER_PROMPTS)
ALL_PROMPTS.update(EVENT_PROMPTS)


def create_workflow(prompt: str, negative: str, filename: str):
    """Создание workflow для ComfyUI API"""
    seed = random.randint(1, 2**53)

    return {
        "39": {
            "class_type": "VAELoader",
            "inputs": {"vae_name": "qwen_image_vae.safetensors"}
        },
        "38": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
                "type": "qwen_image",
                "device": "default"
            }
        },
        "37": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors",
                "weight_dtype": "default"
            }
        },
        "73": {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {
                "model": ["37", 0],
                "lora_name": "Qwen-Image-2512-Lightning-4steps-V1.0-bf16.safetensors",
                "strength_model": 1.0
            }
        },
        "66": {
            "class_type": "ModelSamplingAuraFlow",
            "inputs": {"model": ["73", 0], "shift": 3.1}
        },
        "58": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {"width": 1328, "height": 1328, "batch_size": 1}
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {"clip": ["38", 0], "text": prompt}
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {"clip": ["38", 0], "text": negative}
        },
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["66", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["58", 0],
                "seed": seed,
                "steps": 4,
                "cfg": 1.0,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1.0
            }
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["3", 0], "vae": ["39", 0]}
        },
        "60": {
            "class_type": "SaveImage",
            "inputs": {"images": ["8", 0], "filename_prefix": filename}
        }
    }


def queue_prompt(workflow: dict, session: requests.Session) -> str:
    payload = {"prompt": workflow}
    response = session.post(f"{COMFYUI_URL}/prompt", json=payload)
    return response.json()


def get_history(prompt_id: str, session: requests.Session) -> dict:
    response = session.get(f"{COMFYUI_URL}/history/{prompt_id}")
    return response.json()


def wait_for_completion(prompt_id: str, session: requests.Session, timeout: int = 180):
    start_time = time.time()
    while time.time() - start_time < timeout:
        history = get_history(prompt_id, session)
        if prompt_id in history:
            return history[prompt_id]
        time.sleep(2)
    raise TimeoutError(f"Generation timeout for {prompt_id}")


def download_image(filename: str, session: requests.Session):
    response = session.get(f"{COMFYUI_URL}/view", params={
        "filename": filename,
        "type": "output"
    })
    return response.content


def generate_image(image_id: str, image_data: dict):
    """Генерация одного изображения"""
    print(f"\n[{image_id}] Генерация: {image_data['title']}")
    print(f"    Промпт: {image_data['prompt'][:80]}...")

    session = requests.Session()
    session.trust_env = False

    workflow = create_workflow(
        image_data['prompt'],
        image_data['negative'],
        f"murr_{image_id}"
    )

    try:
        result = queue_prompt(workflow, session)
        prompt_id = result.get('prompt_id')

        if not prompt_id:
            print(f"    ОШИБКА: Не получен prompt_id")
            if 'error' in result:
                print(f"    Детали: {result['error']}")
            return False

        print(f"    Ожидание генерации (ID: {prompt_id})...")

        history = wait_for_completion(prompt_id, session)

        outputs = history.get('outputs', {})
        for node_id, node_output in outputs.items():
            if 'images' in node_output:
                for img in node_output['images']:
                    img_filename = img['filename']
                    img_data = download_image(img_filename, session)

                    output_path = OUTPUT_DIR / f"{image_id}.png"
                    with open(output_path, 'wb') as f:
                        f.write(img_data)

                    print(f"    ГОТОВО: {output_path}")
                    return True

        print(f"    ОШИБКА: Изображение не найдено")
        return False

    except Exception as e:
        print(f"    ОШИБКА: {e}")
        return False


def main():
    print("=" * 60)
    print("Генератор иллюстраций для 'ПЛАНЕТА МУРР'")
    print("Космоопера о котах, драконах и птицах")
    print("=" * 60)
    print(f"ComfyUI: {COMFYUI_URL}")
    print(f"Выходная папка: {OUTPUT_DIR}")
    print(f"Персонажей: {len(CHARACTER_PROMPTS)}")
    print(f"Глав: {len(CHAPTER_PROMPTS)}")
    print(f"Событий: {len(EVENT_PROMPTS)}")
    print(f"ВСЕГО: {len(ALL_PROMPTS)} изображений")
    print("=" * 60)

    session = requests.Session()
    session.trust_env = False

    try:
        response = session.get(f"{COMFYUI_URL}/system_stats", timeout=5)
        if response.status_code != 200:
            print("ОШИБКА: ComfyUI недоступен!")
            return
        print("ComfyUI доступен!\n")
    except Exception as e:
        print(f"ОШИБКА: {e}")
        print("Запустите: wsl -d Ubuntu-24.04 -- bash -c 'cd ~/comfyui && python main.py --listen 0.0.0.0 --port 8190'")
        return

    success = 0
    failed = 0

    # Сначала персонажи
    print("\n=== ПЕРСОНАЖИ ===")
    for img_id, img_data in CHARACTER_PROMPTS.items():
        if generate_image(img_id, img_data):
            success += 1
        else:
            failed += 1
        time.sleep(2)

    # Потом главы
    print("\n=== ГЛАВЫ ===")
    for img_id, img_data in CHAPTER_PROMPTS.items():
        if generate_image(img_id, img_data):
            success += 1
        else:
            failed += 1
        time.sleep(2)

    # Потом события
    print("\n=== СОБЫТИЯ ===")
    for img_id, img_data in EVENT_PROMPTS.items():
        if generate_image(img_id, img_data):
            success += 1
        else:
            failed += 1
        time.sleep(2)

    print("\n" + "=" * 60)
    print(f"ИТОГО: {success} успешно, {failed} ошибок")
    print(f"Изображения в: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
