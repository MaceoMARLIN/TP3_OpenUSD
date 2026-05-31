using UnityEngine;
using UnityEditor;

[InitializeOnLoad]
public class AutoFixOnLoad
{
    static AutoFixOnLoad()
    {
        // Lance le fix après que Unity ait fini de charger
        EditorApplication.delayCall += () =>
        {
            Debug.Log("🔄 Auto-fix des matériaux USD...");
            FixAllMaterials.Fix();
        };
    }
}