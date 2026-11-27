
import mlflow.sklearn

model = mlflow.sklearn.load_model(
    "models/credit_risk_model"
)

print("Model loaded successfully!")
print(type(model))
