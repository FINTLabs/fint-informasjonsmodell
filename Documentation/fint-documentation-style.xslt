<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:UML="omg.org/UML1.3">
  <xsl:output omit-xml-declaration="yes" indent="yes"/>
  <!-- <xsl:strip-space elements="*"/> -->


  <xsl:template match="/">
    <xsl:apply-templates select="document('../FINT-informasjonsmodell.xml')/XMI"/>
  </xsl:template>

  <xsl:template match="XMI">
    <html lang="en">
      <head>
        <meta charset="utf-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title>Dokuementasjon av FINT-informasjonsmodell</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"/>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous"/>
        <style>
          .anchor:before { display: block; content: ""; height: 55px; margin: -55px 0 0; }
          body { padding-top: 50px; }
          .sub-header { padding-bottom: 10px; border-bottom: 1px solid #eee; }
          .navbar-fixed-top { border: 0; }
          .sidebar { display: none; }
          @media (min-width: 768px) {
          .sidebar { position: fixed; top: 51px; bottom: 0; left: 0; z-index: 1000; display: block; padding: 20px; overflow-x: hidden; overflow-y: auto; background-color: #f5f5f5; border-right: 1px solid #eee; }
          }
          .nav-sidebar { margin-right: -21px; margin-bottom: 20px; margin-left: -20px; }
          .nav-sidebar > li > a { padding-right: 20px; padding-left: 20px; }
          .nav-sidebar > .active > a,
          .nav-sidebar > .active > a:hover,
          .nav-sidebar > .active > a:focus { color: #fff; background-color: #428bca; }
          .main { padding: 20px; }
          @media (min-width: 768px) {
          .main { padding-right: 40px; padding-left: 40px; }
          }
          .main .page-header { margin-top: 0; }
          .placeholders { margin-bottom: 30px; text-align: center; }
          .placeholders h4 { margin-bottom: 0; }
          .placeholder { margin-bottom: 20px; }
          .placeholder img { display: inline-block; border-radius: 50%; }
        </style>
        <!--[if lt IE 9]>
          <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
          <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
        <![endif]-->
      </head>
      <body>
        <nav class="navbar navbar-inverse navbar-fixed-top">
          <div class="container-fluid">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="#">Dokumentasjon av informasjonsmodell til FINT</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
              <form class="navbar-form navbar-right">
                <input type="text" class="form-control" placeholder="Search..."/>
              </form>
            </div>
          </div>
        </nav>
        <div class="container-fluid">
          <div class="row">
            <div class="col-sm-3 col-md-2 sidebar">
              <ul class="nav nav-sidebar">
                <xsl:apply-templates select="//UML:ClassifierRole[UML:ModelElement.stereotype]" mode="sidebar-mode"/>
              </ul>
              <ul class="nav nav-sidebar">
                <li><a href=""></a></li>
              </ul>
              
            </div>
            <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
              <h1 class="page-header">Elementer i informasjonsmodellen</h1>
              <xsl:apply-templates select="//UML:Package" mode="packages-mode"/>
            </div>
          </div>
        </div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
      </body>
    </html>
  </xsl:template>
  
  <!-- PACAGE ELEMENT -->
  <xsl:template match="//UML:Package" mode="packages-mode">
    <!-- hack for å fjerne uønskede h2 -->
    <xsl:if test="*/UML:Stereotype">
      <h2 id="package-{@xmi.id}" class="anchor">
        <!-- <span class="glyphicon glyphicon glyphicon-folder-open" aria-hidden="true"></span>-->
        <xsl:text>  </xsl:text>
        <xsl:value-of select="@name"/>
      </h2>
      <i><xsl:value-of select="*/UML:TaggedValue[@tag='documentation']/@value"/></i>
    </xsl:if>
    
    <xsl:apply-templates select="*/UML:Class" mode="class-mode" />
    
  </xsl:template>
  
  <!-- CLASS ELEMENT -->
  <xsl:template match="*/UML:Class" mode="class-mode">
    <xsl:variable name="id" select="@xmi.id"/>
    
    <h3 id="class-{@xmi.id}" class="anchor">
      <span class="glyphicon glyphicon glyphicon-list-alt" aria-hidden="true"></span><xsl:text> </xsl:text>
      <xsl:value-of select="@name"/>
    </h3>
    <p><i><xsl:value-of select="*/UML:TaggedValue[@tag='documentation']/@value"/></i></p>

    <!-- class er en generalisering av -->
    <xsl:if test="//UML:Class[@xmi.id=//UML:Generalization[@subtype=$id]/@supertype]/@name != ''">
      <p>
        <xsl:value-of select="@name"/> er en generalisering av 
        <xsl:for-each select="//UML:Class[@xmi.id=//UML:Generalization[@subtype=$id]/@supertype]">
          <a href="#class-{@xmi.id}">
            <xsl:value-of select="@name"/>
          </a>
          <xsl:if test="position() != last()">
            <xsl:text>, </xsl:text>
          </xsl:if>
        </xsl:for-each>
      </p>
    </xsl:if>

    <!-- class er generalisert som -->
    <xsl:if test="//UML:Class[@xmi.id=//UML:Generalization[@supertype=$id]/@subtype]/@name != ''">
      <p>
        Det finnes følgende generaliseringer av <xsl:value-of select="@name"/>: 
        <xsl:for-each select="//UML:Class[@xmi.id=//UML:Generalization[@supertype=$id]/@subtype]">
          <a href="#class-{@xmi.id}">
            <xsl:value-of select="@name"/>
          </a>
          <xsl:if test="position() != last()">
            <xsl:text>, </xsl:text>
          </xsl:if>
        </xsl:for-each>
      </p>
    </xsl:if>
    
    <!-- felter i en klasse -->
    <table class="table">
      <thead>
        <tr>
          <th>Felt</th>
          <th>Type</th>
          <th>Beskrivelse</th>
        </tr>
      </thead>
      <tbody>
        <xsl:apply-templates select="*/UML:Attribute" mode="attrubute-mode"/>
        <xsl:if test="count(*/UML:Attribute) &lt; 1">
          <tr><td rowspan="3"><em>Har ingen felter.</em></td></tr>
        </xsl:if>
      </tbody>
    </table>

    <!-- assosiasjoner -->
    <table class="table">
      <thead>
        <tr>
          <th>Assosiasjon</th>
          <th>Target</th>
          <th>Relasjon</th>
          <th>Beskrivelse</th>
        </tr>
      </thead>
      <tbody>
        <xsl:apply-templates select="//UML:Association[*/UML:AssociationEnd[*/UML:TaggedValue[@tag='ea_end']/@value = 'source']/@type = $id]" mode="association-mode"/>
        <xsl:if test="count(//UML:Association[*/UML:AssociationEnd[*/UML:TaggedValue[@tag='ea_end']/@value = 'source']/@type = $id]) &lt; 1">
          <tr>
            <td rowspan="3">
              <em>Har ingen assosiasjoner.</em>
            </td>
          </tr>
        </xsl:if>
      </tbody>
    </table>
    
  </xsl:template>

  <xsl:template match="//UML:Association" mode ="association-mode">
    <tr>
      <td>
        <xsl:value-of select="*/UML:TaggedValue[@tag='rt']/@value"/>
      </td>
      <td>
        <a href="#class-{*/UML:AssociationEnd[*/UML:TaggedValue[@tag='ea_end']/@value = 'target']/@type}">
          <xsl:value-of select="*/UML:TaggedValue[@tag='ea_targetName']/@value"/>
        </a>
      </td>
      <td>
        <xsl:value-of select="*/UML:TaggedValue[@tag='rb']/@value"/>
      </td>
      <td>
        <em>
          <xsl:value-of select="*/UML:TaggedValue[@tag='documentation']/@value"/>
        </em>
      </td>
    </tr>
  </xsl:template>
  
  <!-- FIELD/ATTRIBUTE -->
  <xsl:template match="*/UML:Attribute" mode="attrubute-mode">
      <tr>
        <td><xsl:value-of select="@name"/></td>
        <td>
          <xsl:choose>
            <xsl:when test="starts-with(*/UML:Classifier/@xmi.idref, 'EAID')">
              <a href="#class-{*/UML:Classifier/@xmi.idref}"><xsl:value-of select="*/UML:TaggedValue[@tag='type']/@value"/></a>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="*/UML:TaggedValue[@tag='type']/@value"/>
            </xsl:otherwise>
          </xsl:choose>
        </td>
        <td><em><xsl:value-of select="*/UML:TaggedValue[@tag='description']/@value"/></em></td>
      </tr>
  </xsl:template>    
  
  <!-- SIDEBAR ELEMENT -->
  <xsl:template match="//UML:ClassifierRole" mode="sidebar-mode">
      <li><a href="#package-{concat('EAPK_', substring-after(*/UML:TaggedValue[@tag='package2']/@value, '_'))}"><xsl:value-of select="@name"/></a></li>
  </xsl:template>

</xsl:stylesheet>