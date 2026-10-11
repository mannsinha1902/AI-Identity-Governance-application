from src.generate_data import generate
from src.access_recommendations import build_features, train, recommend

def test_ml_pipeline():
    e,g=generate(250)
    features=build_features(e,g)
    model,metrics=train(features)
    result=recommend(model,features)
    assert 0 <= metrics["roc_auc"] <= 1
    assert len(result)==len(g)
    assert result.revoke_score.between(0,1).all()
