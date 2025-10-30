import splitfolders
import os

def split_image_dataset(input_dir, output_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42):
    """
    Splits an image dataset (with class subfolders) into train, validation, and test sets.
    
    Parameters:
    ----------
    input_dir : str
        Path to the original dataset folder (contains subfolders per class)
    output_dir : str
        Path to save the split dataset
    train_ratio : float
        Fraction of images for training set
    val_ratio : float
        Fraction of images for validation set
    test_ratio : float
        Fraction of images for test set
    seed : int
        Random seed for reproducibility

    Returns:
    -------
    output_dir : str
        Path to the folder containing the three split subfolders
    """
    
    # Check ratios
    total = train_ratio + val_ratio + test_ratio
    if total != 1.0:
        raise ValueError(f"Split ratios must sum to 1.0 (got {total})")
    
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Perform the split
    splitfolders.ratio(
        input=input_dir,
        output=output_dir,
        seed=seed,
        ratio=(train_ratio, val_ratio, test_ratio)
    )
    
    print(f"✅ Dataset split completed successfully.")
    print(f"Train, Validation, and Test sets saved to: {output_dir}")
    
    return output_dir


split_image_dataset('D:/Projects/FYP/Brain Tumor Dataset','D:/Projects/FYP/brain_tumor_detection_fyp/Splitted Data Folder')
