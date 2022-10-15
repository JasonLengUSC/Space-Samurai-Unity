using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraScript : MonoBehaviour
{
    public Vector3 Camera_Offset;
    public GameObject Enemy;
    public GameObject Player;
    public GameObject Timer;

    private Animation camAni;

    void Start()
    {
        // Default camera offset
        Camera_Offset = new Vector3(0, 0, -1f);

        // Play starting animation
        camAni = gameObject.GetComponent<Animation>();
        camAni.Play();
        // Stop Anyone from moving before the animation has finished
        Enemy.SetActive(false);
        Player.GetComponent<Movement2D>().enabled = false;
        Timer.GetComponent<Timer_Script>().enabled = false;
        // Debug.Log("Length of Clip = " + Mathf.Ceil(camAni.clip.length));
        StartCoroutine(CountDown((int)Mathf.Ceil(camAni.clip.length)));
        Player.GetComponent<Enemy_Battle_Scripts>().enabled = true;
    }

    // Update is called once per frame
    void Update()
    {
        transform.position = new Vector3(Player.transform.position.x + Camera_Offset.x, Player.transform.position.y + Camera_Offset.y, Camera_Offset.z);
    }


    // Coroutine for Stoping enemies from moving
    private IEnumerator CountDown(int duration)
    {
        yield return new WaitForSeconds(duration);
        Enemy.SetActive(true);
        Player.GetComponent<Movement2D>().enabled = true;
        Timer.GetComponent<Timer_Script>().enabled = true;
        GameObject.Find("Hearts").GetComponent<HealthManager>().EnlargeHeart();
        yield return new WaitForSeconds(1);
        GameObject.Find("Hearts").GetComponent<HealthManager>().ShrinkHearts();
    }
}
