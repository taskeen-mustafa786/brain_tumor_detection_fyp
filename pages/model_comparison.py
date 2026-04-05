"""
Model Comparison page - Test results and model performance comparison
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.model_utils import get_test_results, get_model_comparison

def show():
    """Display model comparison page"""
    st.title("📊 Model Comparison & Test Results")
    
    st.markdown("""
    Comprehensive comparison of all trained models including test results:
    - **Accuracy**: Overall correctness of predictions
    - **Precision**: True positives / (True positives + False positives)
    - **Recall**: True positives / (True positives + False negatives)
    - **F1-Score**: Harmonic mean of Precision and Recall
    - **AUC-ROC**: Area Under the Receiver Operating Characteristic Curve
    """)
    
    st.markdown("---")
    
    # Get test results
    test_results = get_test_results()
    model_comparison = get_model_comparison()
    
    # Create comparison dataframe
    comparison_data = []
    for model in model_comparison['models']:
        comparison_data.append({
            'Model': model['name'],
            'Accuracy': f"{model['accuracy']:.2f}%",
            'Precision': f"{model['precision']:.4f}",
            'Recall': f"{model['recall']:.4f}",
            'F1-Score': f"{model['f1_score']:.4f}",
            'AUC-ROC': f"{model['auc_roc']:.4f}"
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    
    st.subheader("📋 Model Performance Comparison Table")
    st.table(df_comparison)
    
    st.markdown("---")
    
    # Detailed results for each model
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Transfer Learning Model (EfficientNetB0)")
        
        tl_model = test_results['TL_Model']
        
        col_metric1, col_metric2 = st.columns(2)
        with col_metric1:
            st.metric("Accuracy", f"{tl_model['accuracy']:.2f}%", "✅ RECOMMENDED")
            st.metric("Precision", f"{tl_model['precision']:.4f}", "")
            st.metric("Recall", f"{tl_model['recall']:.4f}", "")
        
        with col_metric2:
            st.metric("F1-Score", f"{tl_model['f1_score']:.4f}", "")
            st.metric("AUC-ROC", f"{tl_model['auc_roc']:.4f}", "")
            st.metric("Val Accuracy", f"{tl_model['validation_accuracy']:.2f}%", "")
        
        st.markdown("**Architecture Details:**")
        st.write(f"""
        - **Base Model:** EfficientNetB0 (ImageNet pretrained)
        - **Training Accuracy:** {tl_model['training_accuracy']:.2f}%
        - **Validation Accuracy:** {tl_model['validation_accuracy']:.2f}%
        - **Validation Loss:** {tl_model['validation_loss']:.4f}
        - **Trainable Params:** 1,518,004 (5.79 MB)
        - **Non-trainable Params:** 2,701,171 (10.30 MB)
        - **File:** {tl_model['file']}
        """)
        
        st.success("""
        ✅ **Recommended for Production**
        
        - Exceeds 90% accuracy requirement
        - Best precision and recall
        - Optimal F1-score
        - Lowest validation loss
        - Suitable for clinical deployment
        """)
    
    with col2:
        st.subheader("📊 Custom CNN Model (From Scratch)")
        
        cnn_model = test_results['CNN_Model']
        
        col_metric1, col_metric2 = st.columns(2)
        with col_metric1:
            st.metric("Accuracy", f"{cnn_model['accuracy']:.2f}%", "⚠️ Below target")
            st.metric("Precision", f"{cnn_model['precision']:.4f}", "")
            st.metric("Recall", f"{cnn_model['recall']:.4f}", "")
        
        with col_metric2:
            st.metric("F1-Score", f"{cnn_model['f1_score']:.4f}", "")
            st.metric("AUC-ROC", f"{cnn_model['auc_roc']:.4f}", "")
            st.metric("Val Accuracy", f"{cnn_model['validation_accuracy']:.2f}%", "")
        
        st.markdown("**Architecture Details:**")
        st.write(f"""
        - **Model Type:** Custom CNN built from scratch
        - **Training Accuracy:** {cnn_model['training_accuracy']:.2f}%
        - **Validation Accuracy:** {cnn_model['validation_accuracy']:.2f}%
        - **Validation Loss:** {cnn_model['validation_loss']:.4f}
        - **File:** {cnn_model['file']}
        """)
        
        st.warning("""
        ⚠️ **Alternative Model**
        
        - Below 90% accuracy requirement
        - Lower precision and recall
        - Not recommended for production
        - Can be used as backup/research
        """)
    
    st.markdown("---")
    
    # Visualizations
    st.subheader("📈 Visual Comparison")
    
    tab1, tab2, tab3 = st.tabs(["Metrics Comparison", "Detailed Analysis", "Performance Summary"])
    
    with tab1:
        # Create comparison chart
        models = [m['name'].split('(')[0].strip() for m in model_comparison['models']]
        metrics = {
            'Accuracy': [m['accuracy'] for m in model_comparison['models']],
            'Precision': [m['precision']*100 for m in model_comparison['models']],
            'Recall': [m['recall']*100 for m in model_comparison['models']],
            'F1-Score': [m['f1_score']*100 for m in model_comparison['models']],
            'AUC-ROC': [m['auc_roc']*100 for m in model_comparison['models']]
        }
        
        fig = go.Figure()
        
        for metric, values in metrics.items():
            fig.add_trace(go.Bar(
                name=metric,
                x=models,
                y=values,
                text=[f'{v:.2f}' for v in values],
                textposition='auto',
            ))
        
        fig.update_layout(
            title="Model Performance Metrics Comparison",
            xaxis_title="Model",
            yaxis_title="Score (%)",
            barmode='group',
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Detailed comparison by model
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Transfer Learning Model")
            
            tl_data = {
                'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC', 'Val Loss'],
                'Value': [
                    f"{tl_model['accuracy']:.2f}%",
                    f"{tl_model['precision']:.4f}",
                    f"{tl_model['recall']:.4f}",
                    f"{tl_model['f1_score']:.4f}",
                    f"{tl_model['auc_roc']:.4f}",
                    f"{tl_model['validation_loss']:.4f}"
                ]
            }
            df_tl = pd.DataFrame(tl_data)
            st.table(df_tl)
        
        with col2:
            st.markdown("### Custom CNN Model")
            
            cnn_data = {
                'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC', 'Val Loss'],
                'Value': [
                    f"{cnn_model['accuracy']:.2f}%",
                    f"{cnn_model['precision']:.4f}",
                    f"{cnn_model['recall']:.4f}",
                    f"{cnn_model['f1_score']:.4f}",
                    f"{cnn_model['auc_roc']:.4f}",
                    f"{cnn_model['validation_loss']:.4f}"
                ]
            }
            df_cnn = pd.DataFrame(cnn_data)
            st.table(df_cnn)
    
    with tab3:
        # Radar chart comparison
        st.markdown("### Performance Radar Comparison")
        
        categories = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
        
        tl_values = [
            tl_model['accuracy'],
            tl_model['precision'] * 100,
            tl_model['recall'] * 100,
            tl_model['f1_score'] * 100,
            tl_model['auc_roc'] * 100
        ]
        
        cnn_values = [
            cnn_model['accuracy'],
            cnn_model['precision'] * 100,
            cnn_model['recall'] * 100,
            cnn_model['f1_score'] * 100,
            cnn_model['auc_roc'] * 100
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=tl_values,
            theta=categories,
            fill='toself',
            name='Transfer Learning Model',
            line_color='green'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=cnn_values,
            theta=categories,
            fill='toself',
            name='Custom CNN Model',
            line_color='orange'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            height=500,
            title="Model Performance Radar Comparison"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Test results summary
    st.subheader("📊 Test Results Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Best Model:** Transfer Learning (EfficientNetB0)
        
        ✅ Meets all requirements
        ✅ Highest accuracy: 90.59%
        ✅ Best F1-score: 0.9008
        """)
    
    with col2:
        st.warning("""
        **F1-Score Analysis**
        
        - TL Model: 0.9008 (Excellent)
        - CNN Model: 0.8286 (Good)
        - Difference: 8.7%
        """)
    
    with col3:
        st.warning("""
        **Recall vs Precision**
        
        TL Model achieves:
        - 91.45% Precision
        - 88.76% Recall
        - Balance: Slightly precision-biased
        """)
    
    st.markdown("---")
    
    st.subheader("💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Transfer Learning Advantages
        - ✅ 90.59% validation accuracy
        - ✅ Exceeds 90% SRS requirement
        - ✅ Higher precision (fewer false positives)
        - ✅ Large pre-trained model provides better generalization
        - ✅ Lower validation loss (0.2618)
        - ✅ Recommended for clinical deployment
        """)
    
    with col2:
        st.markdown("""
        ### Custom CNN Limitations
        - ⚠️ 83.37% validation accuracy
        - ⚠️ Below 90% SRS requirement
        - ⚠️ Higher validation loss (0.4112)
        - ⚠️ Lower precision and recall
        - ❌ Not suitable for production
        - ℹ️ Can be used for research/backup
        """)
