import sys
import os
from deeppavlov import build_model, configs
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['figure.figsize'] = (12, 6)


def load_sentiment_model():
    try:
        model = build_model(configs.classifiers.rusentiment_bert, download=True)
        print("[✓] Модель rusentiment_bert успешно загружена")
        return model
    except Exception as e:
        print(f"[×] Ошибка загрузки модели: {str(e)}")
        return None


def main():
    print("=" * 50)
    print("Инициализация модели анализа тональности")
    print("=" * 50)

    sentiment_model = load_sentiment_model()
    if sentiment_model is None:
        return

    print("\n" + "=" * 50)
    print("Загрузка и обработка данных")
    print("=" * 50)

    data_file = "women-clothing-accessories.3-class.balanced.csv"

    if not os.path.exists(data_file):
        print(f"[×] Файл данных '{data_file}' не найден в директории проекта")
        print(f"Текущая рабочая директория: {os.getcwd()}")
        return

    try:
        df = pd.read_csv(data_file, sep='\t')
        print(f"[✓] Данные успешно загружены (всего записей: {len(df)})")
        df = df.head(200).copy()
        print(f"Используется подвыборка из {len(df)} записей для демонстрации")
    except Exception as e:
        print(f"[×] Ошибка загрузки данных: {str(e)}")
        return

    print("\n" + "=" * 50)
    print("Анализ тональности текстов")
    print("=" * 50)

    try:
        print("Выполняется предсказание...")
        df['predicted_sentiment'] = sentiment_model(df['review'].tolist())
        print("[✓] Анализ завершен успешно")
    except Exception as e:
        print(f"[×] Ошибка анализа: {str(e)}")
        return

    if 'sentiment' in df.columns:
        print("\nОценка точности модели:")
        print(classification_report(df['sentiment'], df['predicted_sentiment']))
        accuracy = accuracy_score(df['sentiment'], df['predicted_sentiment'])
        print(f"Общая точность: {accuracy:.2%}")
    else:
        print("\nКолонка 'sentiment' не найдена - оценка точности невозможна")

    print("\n" + "=" * 50)
    print("Визуализация результатов")
    print("=" * 50)

    plt.figure(figsize=(15, 6))
    plt.subplot(1, 2, 1)
    sns.countplot(x='predicted_sentiment', data=df, palette='viridis', order=['negative', 'neutral', 'positive'])
    plt.title('Распределение предсказанных тональностей', pad=20)
    plt.xlabel('Тональность')
    plt.ylabel('Количество отзывов')

    if 'sentiment' in df.columns:
        plt.subplot(1, 2, 2)
        report = classification_report(df['sentiment'], df['predicted_sentiment'], output_dict=True)
        metrics = pd.DataFrame(report).transpose().drop(['accuracy', 'macro avg', 'weighted avg'], errors='ignore')
        sns.heatmap(metrics[['precision', 'recall', 'f1-score']], annot=True, cmap='YlOrBr', fmt='.2f')
        plt.title('Метрики по классам', pad=20)
        plt.yticks(rotation=0)

    plt.tight_layout()
    plt.show()

    output_file = "sentiment_analysis_results.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n[✓] Результаты сохранены в файл: {output_file}")
    print(f"Полный путь: {os.path.abspath(output_file)}")


if __name__ == "__main__":
    main()