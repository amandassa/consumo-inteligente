/**
 * Criado em 24 de ago de 2022
 */
package com.hidrometro;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Random;

import org.eclipse.paho.client.mqttv3.IMqttMessageListener;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.json.JSONException;
import org.json.JSONObject;

import com.clientemqtt.ClienteMQTT;

/**
 * @author Amanda
 */
public class Hidrometro extends Thread {
	private final static int TIME = 5000;
	private final static String NEVOA = "tcp://localhost:1884";
	private int codigo;
	private int vazao;
	private int pressao;
	private int consumo;
	private boolean bloqueado;
	private String dataHora;

	private ClienteMQTT mqtt;
	private String SUB_TOPIC;
	private String PUB_TOPIC;
	
	public Hidrometro(int codigo, int vazao) {
		super();
		this.codigo = codigo;
		this.vazao = vazao;
		this.consumo = 0;
		this.bloqueado = false;
		this.pressao = vazao;
		DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");  
        LocalDateTime now = LocalDateTime.now();
        this.dataHora = dtf.format(now);

		this.mqtt = new ClienteMQTT(NEVOA, null, null);
        this.mqtt.iniciar();
		this.SUB_TOPIC = "hidrometros/bloqueio/"+this.codigo;
		this.PUB_TOPIC = "hidrometros/status/"+this.codigo;

		this.start();
	}
	public static void main (String [] args) {
		Hidrometro h1 = new Hidrometro(new Random().nextInt(20), new Random().nextInt(10));
	}
	
	/**
	 * Envia o status do hidrometro
	 * @return	String de um json serializado
	 */
	public String status () {
		JSONObject jsonObj = new JSONObject();
		try {
			jsonObj.put("codigo",this.codigo);
			jsonObj.put("vazao", this.vazao);
			
			if (this.pressao<this.vazao) {
				jsonObj.put("vazando", true);
			} else {
				jsonObj.put("vazando", false);
			}
			
			jsonObj.put("consumo", this.consumo);
			jsonObj.put("data", this.dataHora);
			jsonObj.put("bloqueado", this.bloqueado);
		} catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		String msg = jsonObj.toString();
		return msg;
	}
	
	
	/**
	 * Abre conexão e mantém escuta ao servidor.
	 * @return JSONObject correspondente ao hidrômetro
	 */
	public void escutar () {
		// um objeto mqttmessagelistener deve subscrever ao broker
		new Ouvinte(this.mqtt, SUB_TOPIC, 0);
	}

	/**
	 * Envia uma mensagem ao servidor
	 * @param mensagem String
	 */
	public void enviar (String mensagem) {
	    try {
			mqtt.publicar(PUB_TOPIC, mensagem.getBytes(), 0);
	    } catch(Exception e) {
	       System.out.println("Erro: " + e.getMessage());
	    }
	}
	
	// public void simulador () {
	// 	int leitor;
	// 	do {
	// 		System.out.println("Altere a pressão da água\nPressão abaixo da média gera alerta de vazamento");
	// 		Scanner sc = new Scanner(System.in);
	//         leitor = sc.nextInt();
	// 		this.pressao = leitor;
	// 		System.out.println("Pressao alterada para "+this.pressao);
	// 		System.out.print("/////////////////////////////////////\r\n");
	// 		sc.close();
	// 	} while (leitor!=13);
    //    sc.next();
	// }
	
	/**
	 * Incrementa o consumo a aprox. cada 1 segundo.
	 */
	@Override
	public void run () {
		Thread escutar = new Thread(() -> escutar());
		// Thread simular = new Thread(() -> simulador());
		try { 
			while (true) {
				try {
					escutar.start();
					// simular.start();
				} catch (java.lang.IllegalThreadStateException e) {
				// caso a thread já esteja em estado de execução
//					System.out.println("Hidrômetro "+this.codigo+" escutando");
				}
				this.consome();
				Thread enviar = new Thread(() -> enviar(status()));
				enviar.start();
				sleep(TIME);
			}
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/**
	 * Incrementa o consumo de acordo com a vazão do hidrômetro.
	 */
	public void consome () {
		if (!this.isBloqueado()) this.setConsumo(this.getConsumo()+this.getVazao());
	}
	
	public int getCodigo() {
		return codigo;
	}
	public void setCodigo(int codigo) {
		this.codigo = codigo;
	}
	public int getVazao() {
		return vazao;
	}
	public void setVazao(int vazao) {
		this.vazao = vazao;
	}
	public int getConsumo() {
		return consumo;
	}
	public void setConsumo(int consumo) {
		this.consumo = consumo;
	}
	public boolean isBloqueado() {
		return bloqueado;
	}
	public void setBloqueado(boolean bloqueado) {
		this.bloqueado = bloqueado;
	}

	public class Ouvinte implements IMqttMessageListener {
		public Ouvinte(ClienteMQTT clienteMQTT, String topico, int qos) {
			clienteMQTT.subscribe(qos, this, topico);
		}
	
		@Override
		public void messageArrived(String topico, MqttMessage mm) throws Exception {
			System.out.println("Mensagem da nevoa:");
			System.out.println("\tTópico: " + topico);
			System.out.println("\tMensagem: " + new String(mm.getPayload()));
			System.out.println("");
			try {
				JSONObject jObject = new JSONObject(mm);

				if (jObject.get("bloqueado").equals(true)) {
					setBloqueado(true);
					System.out.println("HIDROMETRO BLOQUEADO!!!!");
				} else {
					setBloqueado(false);
				}
			}catch (Exception e) {
				e.printStackTrace();
			}
		}
	}
	
}
